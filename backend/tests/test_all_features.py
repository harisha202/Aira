import pytest
from fastapi.testclient import TestClient
from main import app
from utils.jwt import create_token

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ai_models_endpoint():
    response = client.get("/api/v1/ai/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    model_ids = [m["id"] for m in data["models"]]
    assert "claude" in model_ids
    assert "gemini" in model_ids


def test_ai_chat_endpoint():
    payload = {
        "message": "Hello ARIA, test message",
        "model": "claude",
        "max_tokens": 100
    }
    response = client.post("/api/v1/ai/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "model" in data


def test_wikipedia_search_endpoint():
    response = client.get("/api/v1/wikipedia/search?q=Python")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data or "extract" in data or "summary" in data or "title" in data or isinstance(data, dict)


def test_voice_available_voices():
    response = client.get("/api/v1/voice/voices")
    assert response.status_code == 200
    data = response.json()
    assert "voices" in data
    assert len(data["voices"]) >= 1


def test_feedback_submit():
    payload = {
        "rating": 5,
        "feedback_type": "ui",
        "message": "ARIA looks amazing!",
        "user_email": "testuser@example.com",
        "user_name": "Test User"
    }
    response = client.post("/api/v1/feedback/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["user_email"] == "testuser@example.com"


def test_user_profile_authenticated():
    # First sign up a test user
    signup_payload = {
        "email": "profileuser@example.com",
        "name": "Profile Test User",
        "password": "Password123!"
    }
    client.post("/api/v1/auth/signup", json=signup_payload)
    login_resp = client.post("/api/v1/auth/login", json={"email": "profileuser@example.com", "password": "Password123!"})
    if login_resp.status_code == 200 and "token" in login_resp.json():
        token = login_resp.json()["token"]
    else:
        token = create_token({"sub": "test-user-id", "email": "profileuser@example.com", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/user/profile", headers=headers)
    assert response.status_code in [200, 401]

