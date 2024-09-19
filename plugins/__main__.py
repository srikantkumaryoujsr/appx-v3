# @sarkari_student
import asyncio
import importlib
from pyrogram import idle, Client
from plugins import LOGGER, bot as app
from plugins.modules import ALL_MODULES
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

async def _start():
    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)
    
    # Initialize the scheduler with default time
    scheduler.add_job(func=all_subject_send, trigger="cron", hour=6, minute=1, second=0, args=[app])
    
    for all_module in ALL_MODULES:
        importlib.import_module("plugins.modules." + all_module)

    LOGGER.info(f"@{app.username} Started.")
    await app.send_message(7513565186, "I am Alive")
    scheduler.start()  # Start the scheduler
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_start())
    finally:
        loop.close()
    LOGGER.info("Stopping bot")
