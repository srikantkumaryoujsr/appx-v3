from pyrogram import filters
from pyrogram import Client as bot
from pyrogram.types import InlineKeyboardButton as key, InlineKeyboardMarkup as m, Message as msg
import os
import asyncio
import random
import sys
from main import LOGGER, prefixes, Config
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

# Handle the /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_msg(client: bot, message: msg):
    # If the user is a participant, continue with sending the photo and other actions       
    reply_markup = gen_start_kb()
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://te.legra.ph/file/509795aa19e893839762d.jpg",
        caption="❤️𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐛𝐨𝐭! 𝐂𝐡𝐨𝐨𝐬𝐞 𝐚𝐧 𝐨𝐩𝐭𝐢𝐨𝐧❤️:\n\n𝐟𝐨𝐫 𝐑𝐨𝐣𝐠𝐚𝐫 𝐖𝐢𝐭𝐡𝐠 𝐀𝐧𝐤𝐢𝐭 𝐂𝐨𝐮𝐫𝐬𝐞 𝐥𝐢𝐧𝐤 𝐞𝐱𝐭𝐫𝐚𝐜𝐭𝐨𝐫 [𝐓𝐗𝐓 𝐅𝐨𝐫𝐦𝐚𝐭𝐞]",
        reply_markup=reply_markup
    )

def gen_start_kb():
    keyboard = [
        [key("🤦‍♂️𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫🤦‍♂️", url="https://t.me/rojgaarwithankit")],
    ]
    return m(keyboard)
