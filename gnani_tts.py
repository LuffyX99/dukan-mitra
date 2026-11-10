import os
import httpx


async def synthesize(text: str, language: str = "hinglish") -> bytes:
    if os.getenv("MOCK_MODE", "true").lower() == "true":
        return b""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(os.environ["GNANI_TTS_URL"], json={"text": text, "language": language, "stream": True}, headers={"Authorization": f"Bearer {os.environ['GNANI_API_KEY']}"})
        response.raise_for_status()
        return response.content

