from pyrogram import filters
from .. import bot
from pyrogram.types import Message as msg
import os
import asyncio
import random
import sys
from main import LOGGER, prefixes, Config
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

# Remove gen_super_kb function as it generates inline keyboards
# def gen_super_kb(page):
#     ...

async def send_random_photo(bot, chat_id):
    width = random.randint(800, 1600)
    height = random.randint(600, 1200)
    # Removed reply_markup
    await bot.send_photo(
        chat_id=chat_id,
        photo=f"https://picsum.photos/{width}/{height}.jpg",
        caption="**Hi, I am your bot!**\n\nChoose an option:"
    )

@bot.on_message(filters.command("vsbcp"))
async def start_super(bot, message):
    chat_id = message.chat.id
    await send_random_photo(bot, chat_id)

# Remove callback_handler as it handles callback queries
# @bot.on_callback_query()
# async def callback_handler(bot, callback_query):
#     ...

@bot.on_message(filters.command("start") & filters.private)
async def start_msg(bot, message):
    # If the user is a participant, continue with sending the photo and other actions
    reply_mark = gen_start_kb()
    await bot.send_photo(
        message.chat.id,
        photo="https://te.legra.ph/file/4cb09d75328ff12e5be56.jpg",
        caption="**𝐇𝐢, 𝐈 𝐚𝐦 𝐀𝐥𝐢𝐯𝐞..𝐈 𝐚𝐦 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐨𝐫 𝐁𝐨𝐭...𝐢𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐮𝐬𝐞 𝐦𝐞 𝐭𝐡𝐞𝐧 𝐬𝐞𝐧𝐝**\n\n 𝐁𝐨𝐭 𝐦𝐚𝐝𝐞 𝐛𝐲 chutiya",
        reply_markup=reply_mark
    )

def gen_start_kb():
    keyboard = [
        [key("❤️𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫❤️", url="https://t.me/wewq")],
    ]
    return m(keyboard)

@bot.on_message(filters.command(["restart"]))
async def restart_handler(_, message: msg):
    await message.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["log"]))
async def log_msg(bot: bot, message: msg):
    await bot.send_document(message.chat.id, "log.txt")
