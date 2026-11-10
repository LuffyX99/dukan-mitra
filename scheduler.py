import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .analytics import daily_summary
from .gnani_llm import phrase
from .telephony import mock_call

scheduler = AsyncIOScheduler()


async def closing_call() -> dict:
    summary = daily_summary()
    return mock_call(os.getenv("OWNER_NAME", "Ramesh ji"), await phrase(summary, os.getenv("OWNER_LANGUAGE", "hinglish")))


def start_scheduler() -> None:
    hour, minute = map(int, os.getenv("CLOSING_TIME", "21:00").split(":"))
    scheduler.add_job(closing_call, "cron", hour=hour, minute=minute, id="closing-call", replace_existing=True)
    scheduler.start()

