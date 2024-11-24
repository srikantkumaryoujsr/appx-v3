import asyncio
import sys
import config
import requests
import aiohttp
import base64
import pytz
from pytz import utc
from datetime import datetime, timedelta
from pyrogram import Client, filters
from Crypto.Cipher import AES
from .. import bot as Client
from Crypto.Util.Padding import unpad
from .download import account_login
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import requests
import aiohttp
import base64
import pytz
from pytz import utc
from datetime import datetime, timedelta
from pyrogram import filters
from .. import bot as Client
from .. import bot
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from main import AUTH_USERS
from .download import account_login
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait
import os
from plugins.modules.subscription import check_subscription

# MongoDB Configuration
MONGO_URI = "mongodb+srv://aiitassam:SY06t3delyAShe71@cluster0.ugawa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
db = client["bot_database"]
config_collection = db["batch_configs"]

# Global Variables
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
AUTH_USERS = [7224758848,7478730519]
LOG_CHANNEL_ID = -1002336806073

def get_current_date():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def convert_timestamp_to_datetime(timestamp: int) -> str:
    date_time = datetime.utcfromtimestamp(timestamp)
    return date_time.strftime('%Y-%m-%d')

def get_current_date_vsp():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    day_of_week = yesterday.strftime("%A").upper()
    month_name = yesterday.strftime("%B").upper()
    day = yesterday.strftime("%d").zfill(2)
    year = yesterday.strftime("%Y")
    return f"{day}-{month_name}-{year}, {day_of_week}"

async def fetch_data(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

def decrypt_link(link):
    try:
        decoded_link = base64.b64decode(link)
        key = b'638udh3829162018'
        iv = b'fedcba9876543210'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_link = unpad(cipher.decrypt(decoded_link), AES.block_size).decode('utf-8')
        return decrypted_link
    except ValueError as ve:
        print(f"Padding error while decrypting link: {ve}")
    except Exception as e:
        print(f"Error decrypting link: {e}")
        
async def save_config_mongo(batch_name, config_data):
    config_data["subject_and_channel"] = {str(k): v for k, v in config_data["subject_and_channel"].items()}
    await config_collection.update_one({"batch_name": batch_name}, {"$set": config_data}, upsert=True)

async def load_config_mongo():
    cursor = config_collection.find()
    batch_configs = {}
    async for document in cursor:
        batch_name = document.pop("batch_name")
        document["subject_and_channel"] = {int(k): v for k, v in document["subject_and_channel"].items()}
        batch_configs[batch_name] = document
    return batch_configs

async def all_subject_send(bot, bname, batch_configs):
    """Send updates for all subjects in a batch."""
    try:
        batch_config = batch_configs[bname]
        subject_and_channel = batch_config["subject_and_channel"]
        chat_id = batch_config["chat_id"]
        courseid = batch_config["courseid"]
        api_url = batch_config.get("api_url", "https://rozgarapinew.teachx.in")
        token = batch_config.get("token", "default_token_here")

        for subjectid, (chatid, message_thread_id) in subject_and_channel.items():
            try:
                await account_logins(bot, subjectid, chatid, message_thread_id, courseid, bname, api_url, token)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error processing subject {subjectid} in batch {bname}: {e}")

        await bot.send_message(
            chat_id=chatid,
            text=f"**❤️ Class update completed ❤️**\n\n**[ॐ] Date & Day: ➣ {get_current_date_vsp()}**",
            message_thread_id=1
        )

    except Exception as e:
        print(f"Error in all_subject_send: {e}")

async def account_logins(bot, subjectid, chatid, message_thread_id, courseid, bname, api_url, token):
    """Process account logins and handle data."""
    userid = "189678"  # Static user ID for the example
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            res1 = await fetch_data(session, f"{api_url}/get/mycourse?userid={userid}", headers=headers)
            bdetail = res1.get("data", [])
           
            
            all_urls = ""
            couserid = []
            res3 = await fetch_data(session, f"{api_url}/get/alltopicfrmlivecourseclass?courseid={courseid}&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"{api_url}/get/livecourseclassbycoursesubtopconceptapiv3?courseid={courseid}&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
            for c in couserid:
                url = f"{api_url}/get/fetchVideoDetailsById?course_id={courseid}&video_id={c}&ytflag=0&folder_wise_course=0"
                res4 = requests.get(url, headers=hdr1).json()
                video = res4.get("data", [])
                videos.append(video)
              
            for i in videos:
                try:
                    all_important[convert_timestamp_to_datetime(i["strtotime"])] = {
                        "title": i["Title"],
                        'pdf_link': decrypt_link(i['pdf_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link") else "",
                        'pdf_link2': decrypt_link(i['pdf_link2'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link2") else "",
                        'download_link': decrypt_link(i['download_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]).replace("720p", "360p") if i.get("download_link") else ""
                    }
                    
                except Exception:
                    pass
                            
            date = get_current_date()
            if date not in all_important:
                messages = {subjectid: f"{get_current_date_vsp()}\n कल इस Subject की कोई Class नहीं हुआ\n"}
                if subjectid in messages:
                    await bot.send_message(chatid, text=messages[subjectid], message_thread_id=message_thread_id)
                    return

            data = all_important.get(date, {})
            title = data.get("title")
            
            video = data.get("download_link")
            
            pdf_1 = data.get("pdf_link")
            
            pdf_2 = data.get("pdf_link2")
            
            if video:
                all_urls += f"{title}: {video}"
            if pdf_1:
                all_urls += f"\n{title} : {pdf_1}"
            if pdf_2:
                all_urls += f"\n{title} : {pdf_2}"
            
            if all_urls:
                with open(f"{title[:15]}.txt", 'w', encoding='utf-8') as f:
                    f.write(all_urls)

            await bot.send_document(LOG_CHANNEL_ID,
                                    document=f"{title[:15]}.txt",
                                    caption=f"🔴**Batch**🟢: {bname}\n**Subject**: {subjectid}\n**Date**: {get_current_date_vsp()}\n\n")
            print(all_urls)
            await account_login(bot, all_urls, bname, chatid, message_thread_id)
        
        except Exception as e:
            print(f"An error occurred: {e}")

# Scheduler setup
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

# Command to set configuration
@Client.on_message(filters.command("addbatch"))
async def add_batch(bot, message):
    """Add a new batch with configuration."""
    if not check_subscription(message.from_user.id):
        await message.reply_text("**❌ You do not have an active subscription. Contact admin to subscribe.**")
        return
    try:
        parts = message.text.split(" ", 8)
        if len(parts) != 9:
            await message.reply("Error: Invalid format. Use:\n"
                                "`/addbatch bname sujectid:chatid:message_thread_id chat_id courseid hour minute api_url token`")
            return

        bname = parts[1]
        new_subject_and_channel = {}
        for pair in parts[2].split(","):
            subject_id, chat_id, thread_id = map(int, pair.split(":"))
            new_subject_and_channel[subject_id] = (chat_id, thread_id)

        new_chat_id = int(parts[3])
        new_courseid = int(parts[4])
        new_hour = int(parts[5])
        new_minute = int(parts[6])
        new_api_url = parts[7]
        new_token = parts[8]

        new_config = {
            "batch_name": bname,
            "subject_and_channel": new_subject_and_channel,
            "chat_id": new_chat_id,
            "courseid": new_courseid,
            "scheduler_time": {"hour": new_hour, "minute": new_minute},
            "api_url": new_api_url,
            "token": new_token
        }

        await save_config_mongo(bname, new_config)

        batch_configs = await load_config_mongo()
        scheduler.add_job(
            func=all_subject_send,
            trigger=CronTrigger(hour=new_hour, minute=new_minute, second=0, timezone="Asia/Kolkata"),
            args=[bot, bname, batch_configs],
            id=bname
        )

        await message.reply(f"**➕ New batch added successfully!**\n\nBatch Name: {bname}\nAPI URL: {new_api_url}\nToken: {new_token}\n\n"
                            f"To remove this batch, use:\n`/removebatch {bname}`")
        await bot.send_message(
            LOG_CHANNEL_ID,
            f"**➕ New batch added successfully!**\n\nBatch Name: `{bname}`\nAPI URL: `{new_api_url}`\nToken: `{new_token}`\n\n"
            f"To remove this batch, use:\n`/removebatch {bname}`"
        )

    except Exception as e:
        await message.reply(f"Error adding batch: {e}")

@Client.on_message(filters.command("viewbatches"))
async def view_batches(bot, message):
    batch_configs = await load_config_mongo()
    if not batch_configs:
        await message.reply("No batches configured.")
        return

    response = "**🟢ᴄᴜʀʀᴇɴᴛ ꜱᴄʜᴇᴅᴜʟᴇᴅ ᴄᴏᴜʀꜱᴇꜱ🟠**\n\n"
    for bname, details in batch_configs.items():
        schedule_time = details.get("scheduler_time", {})
        hour = schedule_time.get("hour")
        minute = schedule_time.get("minute")
        schedule_display = f"{hour:02d}:{minute:02d} IST" if hour is not None else "Not Set"
        response += f"**Batch Name:** `{bname}`\n"
        response += f"**Scheduled Time:** {schedule_display}\n"
        response += f"**☢️ɪꜰ ʏᴏᴜ ʀᴇᴍᴏᴠᴇ ᴛʜɪꜱ ʙᴀᴛᴄʜ ᴄᴏᴘʏ ʙᴇʟᴏᴡ ᴛᴇxᴛ☢️**\n`/removebatch {bname}`\n"
        response += "====================\n\n"

    await message.reply(response)

@Client.on_message(filters.command("removebatch"))
async def remove_batch(bot, message):
    """Remove a batch and its configuration."""
    try:
        parts = message.text.split(" ", 1)
        if len(parts) != 2:
            await message.reply("Error: Invalid format. Use: `/removebatch bname`")
            return

        bname = parts[1]

        batch_collection.delete_one({"batch_name": bname})
        scheduler.remove_job(bname)

        await message.reply(f"**➖ Batch '{bname}' removed successfully!**")
        await bot.send_message(LOG_CHANNEL_ID, f"**➖ Batch '{bname}' removed successfully!**")

    except Exception as e:
        await message.reply(f"Error removing batch: {e}")

async def load_batches_on_start():
    try:
        batch_configs = await load_config_mongo()
        for bname, config in batch_configs.items():
            schedule_time = config["scheduler_time"]
            scheduler.add_job(
                func=all_subject_send,
                trigger=CronTrigger(hour=schedule_time["hour"], minute=schedule_time["minute"], second=0, timezone="Asia/Kolkata"),
                args=[Client, bname, batch_configs],
                id=bname
            )
            print(f"Scheduled batch '{bname}' at {schedule_time['hour']}:{schedule_time['minute']} IST.")
    except Exception as e:
        print(f"Error loading batches on startup: {e}")
        
scheduler.start()

@Client.on_message(filters.command("restart"))
async def restart_bot(bot, message):
    if not check_subscription(message.from_user.id):
        await message.reply_text("**❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴**\n\n**🟡☢️ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ꜱᴜʙꜱᴄʀɪʙᴇ.🔵❤️**")
        return
    try:
        await message.reply("🟠🟢𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐜𝐟𝐮𝐥𝐥𝐲🔴✅")
        # Save any critical data or perform cleanup if necessary here
        
        # Restart the bot using execv
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        await message.reply(f"Failed to restart the bot: {e}")
