from pyrogram import filters
from pyrogram import Client as bot
from pyrogram.types import Message as msg
import os
import asyncio
import random
import sys
from main import LOGGER, prefixes, Config
from pyrogram.errors import ChatWriteForbidden

# Handle the /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_msg(client: bot, message: msg):
    try:
        await message.reply(
            "❤️ Welcome to the bot! ❤️\n\nChoose an option:\n\nFor Rojgar With Ankit Course link extractor [TXT Format]"
        )
    except ChatWriteForbidden:
        await message.reply("Sorry, I don't have permission to write in this chat.")
    except Exception as e:
        LOGGER.error(f"Failed to send start message: {e}")
        await message.reply("An error occurred. Please try again later.")
