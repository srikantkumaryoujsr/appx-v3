#@sarkari_student
import asyncio
import importlib
from pyrogram import idle
from plugins import LOGGER, bot as app
from plugins.modules import ALL_MODULES

async def _start():
    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)
    for all_module in ALL_MODULES:
        importlib.import_module("plugins.modules." + all_module)

    LOGGER.info(f"@{app.username} Started.")
    await app.send_message(6881758615, "I am Alive")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_start())
    finally:
        loop.close()
    LOGGER.info("Stopping bot")
