import asyncio
import httpx
import json

async def test_all():
    async with httpx.AsyncClient() as client:
        print("==============================")
        print("1. Testing AI Models Endpoint")
        print("==============================")
        models_resp = await client.get("http://localhost:8000/api/v1/ai/models")
        print("Available Models:", models_resp.json())
        
        print("\n==============================")
        print("2. Testing Gemini API")
        print("==============================")
        payload = {
            "conversation_id": "test-123",
            "message": "Please reply with the exact word: GEMINI",
            "model_override": "gemini"
        }
        resp = await client.post("http://localhost:8000/api/v1/ai/chat", json=payload)
        print("Gemini Response:", resp.json())
        
        print("\n==============================")
        print("3. Testing Claude API")
        print("==============================")
        payload["message"] = "Please reply with the exact word: CLAUDE"
        payload["model_override"] = "claude"
        resp = await client.post("http://localhost:8000/api/v1/ai/chat", json=payload)
        print("Claude Response:", resp.json())
        
        print("\n==============================")
        print("4. Testing Wikipedia Integration")
        print("==============================")
        # Assuming wikipedia is routed when the message starts with /wiki
        payload["message"] = "/wiki Artificial Intelligence"
        resp = await client.post("http://localhost:8000/api/v1/chat/send-message", json={"message": "/wiki Artificial Intelligence", "conversation_id": "test-wiki", "user_id": "guest"})
        
        if resp.status_code == 200:
            print("Wikipedia Route Success. Response keys:", resp.json().keys())
            if "ai_message" in resp.json():
                print("Wikipedia Extract Snippet:", resp.json()["ai_message"]["content"][:150] + "...")
        else:
            print("Wikipedia request failed:", resp.status_code, resp.text)
            
        print("\n==============================")
        print("5. Testing Voice Synthesis (TTS)")
        print("==============================")
        tts_payload = {"text": "Testing voice synthesis.", "voice_name": "default"}
        tts_resp = await client.post("http://localhost:8000/api/v1/voice/synthesize", json=tts_payload)
        if tts_resp.status_code == 200:
            print("TTS Response successful! Audio Base64 received, length:", len(tts_resp.json().get("audio_base64", "")))
        else:
            print("TTS Failed:", tts_resp.status_code, tts_resp.text)

if __name__ == "__main__":
    asyncio.run(test_all())
