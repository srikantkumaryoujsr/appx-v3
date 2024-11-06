import logging
from pyrogram import filters
from pyrogram import Client as bot
from pyrogram.types import Message as msg
from pyrogram.errors import ChatWriteForbidden

# Configure logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Handle the /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_msg(client: bot, message: msg):
    LOGGER.info(f"Received /start command from user {message.from_user.id}")
    
    try:
        await message.reply(
            "❤️ Welcome to the bot! ❤️\n\nChoose an option:\n\nFor Rojgar With Ankit Course link extractor [TXT Format]"
        )
        LOGGER.info("Sent start message successfully.")
    except ChatWriteForbidden:
        LOGGER.warning("Bot lacks write permission in the chat.")
        await message.reply("Sorry, I don't have permission to write in this chat.")
    except Exception as e:
        LOGGER.error(f"Failed to send start message: {e}")
        await message.reply("An error occurred. Please try again later.")
