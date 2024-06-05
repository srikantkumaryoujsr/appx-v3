from pyrogram import filters
from .. import bot
from pyrogram.types import InlineKeyboardButton as key, InlineKeyboardMarkup as m, Message as msg, CallbackQuery
import os
import asyncio
import random
import sys
from main import LOGGER, prefixes, Config
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

def gen_super_kb(page):
    if page == 1:
        keyboard = [
            [key("🩵E1 Cᴏᴀᴄʜɪɴɢ🩵", callback_data=f"e1_e1coachingcenterapi.classx.co.in"), key("🩵Mɢ Cᴏɴᴄᴇᴘᴛ🩵", callback_data=f"mg_mgconcept.classx.co.in")],
            [key("🩷 Aᴘɴɪ Pᴀᴛʜsᴀʟᴀ 🩷", callback_data="e2_e1coachingcenterapi.classx.co.in"), key("🩷Rᴊ Vɪᴋʀᴀᴍᴊᴇᴇᴛ🩷", callback_data="cds")],           
            [key("📍Cᴀʀᴇᴇʀ Wɪʟʟ📍", callback_data="cds")],
            [key("📍 Kᴅ Cᴀᴍᴘᴜs 📍", callback_data="cds")],
            [key("❤️ Uᴄ Lɪᴠᴇ ❤️", callback_data="cds"), key("❤️ Sᴛᴜᴅʏ Lᴀʙ ❤️", callback_data="cds")],
            [key("🩷 Sᴛᴜᴅʏ Mᴀɴᴛʀᴀ 🩷", callback_data="cds"), key("🩷 Sᴀᴍʏᴀᴋ 🩷", callback_data="cds")],           
            [key("🔰 Pʜʏsɪᴄs Wᴀʟʟᴀʜ 🔰", callback_data="cds")],
            [key("🔰 Cʟᴀss Pʟᴜs 🔰", callback_data="cds")],
            [key("⏩Nᴇxᴛ Pᴀɢᴇ➡️", callback_data="next_page_1")]
        ]
    elif page == 2:
        keyboard = [
            [key("🩵 Oᴄᴇᴀɴ 🩵", callback_data="cds"), key("🩵 Wɪɴɴᴇʀ 🩵", callback_data="cds")],
            [key("🩷 Vᴇᴅ Pʀᴇᴘ 🩷", callback_data="cds"), key("🩷Cᴀᴅᴇᴛ Dᴇғᴇɴᴄᴇ Aᴄᴀ•🩷", callback_data="cds")],           
            [key("📍Cᴅs Jᴏᴜʀɴᴇʏ📍", callback_data="cds")],
            [key("📍Iɴsɪɢʜᴛ Ssʙ📍", callback_data="cds")],
            [key("❤️Rᴏᴊɢᴀʀ Wɪᴛʜ Aɴᴋɪᴛ❤️", callback_data="cds"), key("❤️ Cʜᴀɴᴅᴀɴ Lᴏɢɪᴄ ❤️", callback_data="cds")],
            [key("🩷 Exᴀᴍᴏ 🩷", callback_data="cds"), key("🩷 Gʏᴀɴ Bɪɴᴅᴜ 🩷", callback_data="cds")], 
            [key("🩷 Back 🩷", callback_data="back_page_2"), key("⏩Home➡️", callback_data="home"), key("⏩Nᴇxᴛ Pᴀɢᴇ➡️", callback_data="next_page_2")]
        ]
    elif page == 3:
        keyboard = [
            [key("🩵 xxxxxx 🩵", callback_data="cds"), key("🩵 Wɪɴɴᴇʀ 🩵", callback_data="cds")],
            [key("🩷 Vᴇᴅ Pʀᴇᴘ 🩷", callback_data="cds"), key("🩷Cᴀᴅᴇᴛ Dᴇғᴇɴᴄᴇ Aᴄᴀ•🩷", callback_data="cds")],           
            [key("📍Cᴅs Jᴏᴜʀɴᴇʏ📍", callback_data="cds")],
            [key("📍Iɴsɪɢʜᴛ Ssʙ📍", callback_data="cds")],
            [key("❤️Rᴏᴊɢᴀʀ Wɪᴛʜ Aɴᴋɪᴛ❤️", callback_data="cds"), key("❤️ Cʜᴀɴᴅᴀɴ Lᴏɢɪᴄ ❤️", callback_data="cds")],
            [key("🩷 Exᴀᴍᴏ 🩷", callback_data="cds"), key("🩷 Gʏᴀɴ Bɪɴᴅᴜ 🩷", callback_data="cds")], 
            [key("🩷 Home 🩷", callback_data="back_page_3"), key("⏩Nᴇxᴛ Pᴀɢᴇ➡️", callback_data="home"), key("⏩Nᴇxᴛ Pᴀɢᴇ➡️", callback_data="next_page_3")]
        ]
    else:
        keyboard = [
            [key("🩷 Home 🩷", callback_data="home")], 
            [key("⏩Nᴇxᴛ Pᴀɢᴇ➡️", callback_data="next_page_3"), key("⏩Nᴇxᴛ Pᴀɢᴇ➡️", callback_data="next_page_3")]
        ]
    return m(keyboard)
async def send_random_photo(bot, chat_id):
    width = random.randint(800, 1600)
    height = random.randint(600, 1200)
    reply_mark = gen_start_kb()
    await bot.send_photo(
        chat_id=chat_id,
        photo=f"https://picsum.photos/{width}/{height}.jpg",
        caption="**Hi, I am your bot!**\n\nChoose an option:",
        reply_markup=reply_mark
    )


@bot.on_message(filters.command("vsbcp"))
async def start_super(bot, message):
    chat_id = message.chat.id
    await send_random_photo(bot, chat_id)
async def send_random_photo(bot, chat_id):
    width = random.randint(800, 1600)
    height = random.randint(600, 1200)
    page = 1 
    reply_markup = gen_super_kb(page)
    await bot.send_photo(
        chat_id=chat_id,
        photo=f"https://picsum.photos/{width}/{height}.jpg",
        caption="**Hi, I am your bot!**\n\nChoose an option:",
        reply_markup=reply_markup
    )

@bot.on_callback_query()
async def callback_handler(bot, callback_query):
    data = callback_query.data
    if data.startswith("e1_"):
        api_endpoint = data.split("_")[1]  # Extract the API endpoint
        await callback_query.answer("You chose E1 Coaching ")
        await e1.handle_appx_logic(bot, callback_query.message, api_endpoint)
    elif data.startswith("e2_"):
        api_endpoint = data.split("_")[1]  
        user_id = callback_query.from_user.id if callback_query.from_user is not None else None
        print(user_id)
        await callback_query.answer("You chose E1 Coaching")
        await appxv2.handle_appxv2_logic(bot, callback_query.message, api_endpoint)
    elif data == "e1":
        await callback_query.answer("You chose E1 Coaching ")
        await cds.handle_appx_logic(bot, callback_query.message)
    elif data == "cds":
        await callback_query.answer("You chose CDS")
        await cds.handle_cds_logic(bot, callback_query.message)
    elif data == "e1":
        await callback_query.answer("You chose E1 Coaching ")
        await cds.handle_appx_logic(bot, callback_query.message)
    elif data == "home":
        page = 1
        reply_markup = gen_super_kb(page)
        await callback_query.message.edit_reply_markup(reply_markup)
    elif data.startswith("back_page"):
        page = int(data.split("_")[-1]) - 1
        reply_markup = gen_super_kb(page)
        await callback_query.message.edit_reply_markup(reply_markup)
    elif data.startswith("next_page"):
        page = int(data.split("_")[-1]) + 1
        reply_markup = gen_super_kb(page)
        await callback_query.message.edit_reply_markup(reply_markup)
@bot.on_message(filters.command("start") & filters.private)
async def start_msg(bot, message):
    # If the user is a participant, continue with sending the photo and other actions       
    reply_mark = gen_start_kb()
    await bot.send_photo(
        message.chat.id,
        photo="http://graph.org/file/3d4121f27426f00e58063.jpg",
        caption="**𝐇𝐢, 𝐈 𝐚𝐦 𝐀𝐥𝐢𝐯𝐞..𝐈 𝐚𝐦 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐨𝐫 𝐁𝐨𝐭...𝐢𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐮𝐬𝐞 𝐦𝐞 𝐭𝐡𝐞𝐧 𝐬𝐞𝐧𝐝**\n\n 𝐁𝐨𝐭 𝐦𝐚𝐝𝐞 𝐛𝐲 @sarkari_student",
        reply_markup=reply_mark
    )
        
def gen_start_kb():
    keyboard = [
        [key("❤️𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫❤️", url="https://t.me/SARKARI_STUDENT")],           
        
    ]
    return m(keyboard)



@bot.on_message(filters.command(["restart"]))
async def restart_handler(_, message):
    await message.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["log"]))
async def log_msg(bot: bot , message: msg):   
    await bot.send_document(message.chat.id, "log.txt")
