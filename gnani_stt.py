import os
import httpx


async def transcribe(audio: bytes, language: str = "hinglish") -> dict:
    if os.getenv("MOCK_MODE", "true").lower() == "true":
        return {"text": "", "confidence": 1.0, "language": language}
    url = os.environ["GNANI_STT_URL"]
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, content=audio, headers={"Authorization": f"Bearer {os.environ['GNANI_API_KEY']}"}, params={"language": language, "stream": "true"})
        response.raise_for_status()
        return response.json()

