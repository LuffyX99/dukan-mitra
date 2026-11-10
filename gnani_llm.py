import os
import httpx
from .languages import reply


async def phrase(summary: dict, language: str = "hinglish") -> str:
    if os.getenv("MOCK_MODE", "true").lower() == "true":
        return reply(language, "summary", sales=f"{summary['total_sales_today']:.0f}", low=len(summary["low_stock"]))
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(os.environ["GNANI_EVON_URL"], json={"summary": summary, "language": language, "max_words": 25}, headers={"Authorization": f"Bearer {os.environ['GNANI_API_KEY']}"})
        response.raise_for_status()
        return response.json()["text"]

