import asyncio
import httpx

async def test_ai():
    async with httpx.AsyncClient() as client:
        print("Testing models endpoint...")
        models_resp = await client.get("http://localhost:8000/api/v1/ai/models")
        print("Models:", models_resp.json())
        
        print("\nTesting Gemini generation...")
        payload = {
            "conversation_id": "test-123",
            "message": "Hello, this is a test. Please reply with the single word: OK",
            "model_override": "gemini"
        }
        resp = await client.post("http://localhost:8000/api/v1/ai/chat", json=payload)
        print("Gemini response:", resp.json())
        
        print("\nTesting Claude generation...")
        payload["model_override"] = "claude"
        resp = await client.post("http://localhost:8000/api/v1/ai/chat", json=payload)
        print("Claude response:", resp.json())

if __name__ == "__main__":
    asyncio.run(test_ai())
