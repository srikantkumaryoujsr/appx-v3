import asyncio
import requests
import aiohttp
import base64
import pytz
from datetime import datetime, timedelta
from pyrogram import filters
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from .. import bot as Client
from .. import bot
from main import AUTH_USERS
from .download import account_login
from pyrogram.errors import FloodWait

# MongoDB सेटअप (अपने अनुसार URL और credentials अपडेट करें)
client = MongoClient("mongodb+srv://sarkari226:Nzp4hfYpAdoo2dYH@cluster0.lavidof.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["course_database"]
course_collection = db["courses"]

# कॉन्फ़िगरेशन
AUTH_USERS.extend([7224758848])
LOG_CHANNEL_ID = -1002004338182

# समय क्षेत्र की सेटिंग
def get_current_date():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def get_current_date_vsp():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    day_of_week = yesterday.strftime("%A").upper()
    month_name = yesterday.strftime("%B").upper()
    day = yesterday.strftime("%d").zfill(2)
    year = yesterday.strftime("%Y")
    return f"{day}-{month_name}-{year}, {day_of_week}"

def convert_timestamp_to_datetime(timestamp: int) -> str:
    date_time = datetime.utcfromtimestamp(timestamp)
    return date_time.strftime('%Y-%m-%d')

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
    except Exception as e:
        print(f"Error decrypting link: {e}")

# नया कोर्स जोड़ने के लिए `/add_course` कमांड
@Client.on_message(filters.command("add_course") & filters.user(AUTH_USERS))
async def add_course_command(bot, message):
    try:
        await message.reply("कृपया subject_and_channel (उदाहरण: {1142: (-1002289423851, 2), ...}) इनपुट करें:")
        response = await bot.listen(message.chat.id)
        subject_and_channel = eval(response.text)
        
        await message.reply("कृपया chat_id इनपुट करें:")
        response = await bot.listen(message.chat.id)
        chat_id = int(response.text)
        
        await message.reply("कृपया courseids इनपुट करें:")
        response = await bot.listen(message.chat.id)
        courseids = response.text
        
        await message.reply("कृपया scheduler hour इनपुट करें:")
        response = await bot.listen(message.chat.id)
        hour = int(response.text)
        
        await message.reply("कृपया scheduler minute इनपुट करें:")
        response = await bot.listen(message.chat.id)
        minute = int(response.text)
        
        # MongoDB में कोर्स डेटा सेव करें
        course_data = {
            "subject_and_channel": subject_and_channel,
            "chat_id": chat_id,
            "courseids": courseids,
            "scheduler_time": {"hour": hour, "minute": minute}
        }
        course_collection.insert_one(course_data)
        
        await message.reply("नया कोर्स सफलतापूर्वक जोड़ा गया और सेव हो गया!")
    
    except Exception as e:
        await message.reply(f"कोर्स जोड़ने में त्रुटि: {e}")

# सभी कोर्स के लिए शेड्यूलर सेटअप
def schedule_all_courses():
    scheduler.remove_all_jobs()
    courses = course_collection.find()
    for course in courses:
        scheduler.add_job(
            func=all_subject_send,
            trigger=CronTrigger(
                hour=course['scheduler_time'].get('hour', 0),    # Default to 0 if not provided
                minute=course['scheduler_time'].get('minute', 0),  # Default to 0 if not provided
                second=course['scheduler_time'].get('second', 0),  # Default to 0 if not provided
                timezone="Asia/Kolkata"
            ),
            args=[course["subject_and_channel"], course["chat_id"], course["courseids"]]
        )
        logger.info("कोर्स शेड्यूल किया गया: %s", course)

# सभी कोर्स को भेजने के लिए मुख्य फंक्शन
async def all_subject_send(subject_and_channel, chat_id, courseids):
    for subjectid, (chatid, message_thread_id) in subject_and_channel.items():
        try:
            await account_logins(subjectid, chatid, message_thread_id, courseids)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await account_logins(subjectid, chatid, message_thread_id, courseids)
        except Exception as e:
            print(f"Error processing subject {subjectid}: {e}")

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=f"**❤️ᴅᴇᴀʀ ꜱᴛᴜᴅᴇɴᴛ ᴀᴀᴘᴋɪ ᴄʟᴀꜱꜱ ᴜᴘᴅᴀᴛᴇ ʜᴏ ɢɪ ʜᴀɪ ❤️**\n\n**[ॐ] ᴅᴀᴛᴇ & ᴅᴀʏ : ➣ {get_current_date_vsp()}**\n\n**ʀᴇᴀᴄᴛɪᴏɴ❤️**", 
            message_thread_id=1
        )
    except Exception as e:
        print(f"Failed to send end message: {e}")

# account_logins फंक्शन को अपडेट करें
async def account_logins(subjectid, chatid, message_thread_id, courseids):
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
            bname = bdetail[0]["course_name"] if bdetail else "No Course"
            
            all_urls = ""
            couserid = []
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid={courseids}&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            topicids = [i["topicid"] for i in topic]
            videos = []
            all_important = {}
            
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid={courseids}&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                for i in videodata:
                    couserid.append(i["id"])
            
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id={courseids}&video_id={c}&ytflag=0&folder_wise_course=0"
                res4 = requests.get(url, headers=hdr1).json()
                video = res4.get("data", [])
                videos.append(video)
            
            for i in videos:
                try:
                    all_important[convert_timestamp_to_datetime(i["strtotime"])] = {
                        "title": i["Title"],
                        'pdf_link': decrypt_link(i['pdf_link']) if i.get("pdf_link") else "",
                        'pdf_link2': decrypt_link(i['pdf_link2']) if i.get("pdf_link2") else "",
                        'download_link': decrypt_link(i['download_link']).replace("720p", "720p") if i.get("download_link") else ""
                    }
                except Exception:
                    pass
            
            date = get_current_date()
            if date not in all_important:
                await bot.send_message(chatid, text=f"{get_current_date_vsp()}\n कल इस Subject की कोई Class नहीं हुआ", message_thread_id=message_thread_id)
                return
            
            data = all_important.get(date, {})
            title = data.get("title")
            video = data.get("download_link")
            pdf_1 = data.get("pdf_link")
            pdf_2 = data.get("pdf_link2")
            
            all_urls = f"{title}: {video}\n{'[1]' + pdf_1 if pdf_1 else ''} | {'[2]' + pdf_2 if pdf_2 else ''}\n"
            await bot.send_message(chatid, text=all_urls, message_thread_id=message_thread_id)
        
        except Exception as e:
            print(f"Failed to process course data: {e}")

# शेड्यूलर शुरू करें और सभी कोर्स शेड्यूल करें
scheduler = AsyncIOScheduler()
scheduler.start()
schedule_all_courses()
