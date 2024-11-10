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
AUTH_USERS.extend([7224758848])
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB Configuration
MONGO_URI = "mongodb+srv://heeokumailseptember:nfOkF8F4zn1FIAFQ@cluster0.xb62l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "bot_config"
COLLECTION_NAME = "batch_configs"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
batch_collection = db[COLLECTION_NAME]

LOG_CHANNEL_ID = -1002004338182

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

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

@Client.on_message(filters.command("startnow1") & filters.user(AUTH_USERS))
async def start_subjects_command(bot, message):
    batches = await batch_collection.find().to_list(length=None)
    for batch in batches:
        await all_subject_send(bot, batch["bname"])

async def all_subject_send(bot, bname):
    batch = await batch_collection.find_one({"bname": bname})
    if not batch:
        print(f"Batch {bname} not found.")
        return

    subject_and_channel = batch["subject_and_channel"]
    chat_id = batch["chat_id"]
    courseid = batch["courseid"]

    for subjectid, (chatid, message_thread_id) in subject_and_channel.items():
        try:
            await account_logins(bot, subjectid, chatid, message_thread_id, courseid, bname)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"Error processing subject {subjectid} in batch {bname}: {e}")

    await bot.send_message(
        chat_id=chat_id,
        text=f"**❤️ क्लास अपडेट हो गई है ❤️**\n\n**[ॐ] Date & Day: ➣ {get_current_date_vsp()}**",
        message_thread_id=1
    )

async def account_logins(bot, subjectid, chatid, message_thread_id, courseid, bname):
    # Implement your account login logic here
    pass
    userid = "189678"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQzMDIyMzEiLCJlbWFpbCI6InNhdXJhYmhrYXVzaGlrc2hhcm1hc0BnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MTUxNDg3ODl9.YHQvtTXSjEsaytQI1p2TVzb0faIm5R3e96LVKtCsZQU"
            hdr1 = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
           
            
            all_urls = ""
            couserid = []
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid={courseid}&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid={courseid}&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id={courseid}&video_id={c}&ytflag=0&folder_wise_course=0"
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
                messages = {f"{get_current_date_vsp()}\n कल इस Subject की कोई Class नहीं हुआ\n"}
                
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
            print(all_urls)
            await account_login(bot, all_urls, bname, chatid, message_thread_id)
        
        except Exception as e:
            print(f"An error occurred: {e}")

# Scheduler setup
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

# Command to set configuration
@Client.on_message(filters.command("addbatch"))
async def add_batch(bot, message):
    try:
        parts = message.text.split(" ", 6)
        if len(parts) != 7:
            await message.reply("Error: Invalid format. Use:\n"
                                "`/addbatch bname subject_and_channel chat_id courseid hour minute`")
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

        batch_data = {
            "bname": bname,
            "subject_and_channel": new_subject_and_channel,
            "chat_id": new_chat_id,
            "courseid": new_courseid,
            "scheduler_time": {"hour": new_hour, "minute": new_minute}
        }

        await batch_collection.update_one({"bname": bname}, {"$set": batch_data}, upsert=True)

        scheduler.add_job(
            func=all_subject_send,
            trigger=CronTrigger(hour=new_hour, minute=new_minute, second=0, timezone="Asia/Kolkata"),
            args=[bot, bname],
            id=bname,
            replace_existing=True
        )

        await message.reply(f"New batch added: {bname}")

    except Exception as e:
        await message.reply(f"Error adding batch: {e}")

@Client.on_message(filters.command("viewbatches"))
async def view_batches(bot, message):
    batches = await batch_collection.find().to_list(length=None)
    if not batches:
        await message.reply("No batches configured.")
        return

    response = "**🦋𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐁𝐚𝐭𝐜𝐡𝐞𝐬🦋:**\n\n"
    for batch in batches:
        schedule_time = batch.get("scheduler_time", {})
        hour = schedule_time.get("hour", "N/A")
        minute = schedule_time.get("minute", "N/A")
        response += f"**Batch Name:** `{batch['bname']}`\n"
        response += f"**Scheduled Time:** {hour:02d}:{minute:02d} IST\n"
        response += "====================\n"
    await message.reply(response)

@Client.on_message(filters.command("removebatch"))
async def remove_batch(bot, message):
    try:
        parts = message.text.split(" ", 1)
        if len(parts) != 2:
            await message.reply("Error: Invalid format. Use:\n"
                                "`/removebatch bname`")
            return

        bname = parts[1]
        result = await batch_collection.delete_one({"bname": bname})

        if result.deleted_count == 0:
            await message.reply(f"Batch '{bname}' not found.")
            return

        scheduler.remove_job(bname)
        await message.reply(f"Batch '{bname}' removed successfully.")

    except Exception as e:
        await message.reply(f"Error removing batch: {e}")

# Start the scheduler
scheduler.start()
