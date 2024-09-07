import asyncio
import aiohttp
import base64
import pytz
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pyrogram import filters
from .. import bot as Client
from .. import bot
from main import AUTH_USERS
from .download import account_login
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait

AUTH_USERS.extend([6748451207, 6804421130, 6671207610, 6741261680])

def get_current_date():
    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    return formatted_date

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
    except (ValueError, Exception) as e:
        print(f"Decryption failed: {e}")
        return ""

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

async def all_subject_send(bot):
    subject_and_channel = {
        828: -1002344440579, 
        832: -1002344440579, 
        958: -1002344440579, 
        1043: -1002344440579, 
        1050: -1002344440579
    }
    
    try:
        # Send start message
        start_message = await bot.send_message(chat_id=-1002344440579, text="📢 Processing has started for the subjects!")
        
        async def pin_latest_message():
            try:
                # Fetch the latest message from the channel
                updates = await bot.get_chat_history(chat_id=-1002344440579, limit=1)
                if updates:
                    latest_message_id = updates[0].message_id

                    # Pin the latest message
                    await bot.pin_chat_message(chat_id=-1002344440579, message_id=latest_message_id, disable_notification=False)
                    print(f"Message {latest_message_id} pinned.")
            except Exception as e:
                print(f"Failed to pin message: {e}")

        for subjectid, chatid in subject_and_channel.items():
            try:
                await account_logins(bot, subjectid, chatid)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await account_logins(bot, subjectid, chatid)
            except Exception as e:
                print(f"Error processing subject {subjectid}: {e}")

        try:
            await bot.send_message(chat_id=-1002344440579, text=f"✅ Processing has completed for the subjects!\n\nDate :- **{get_current_date()}**")
        except Exception as e:
            print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid):
    userid = "1245678"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzODgwMDEiLCJlbWFpbCI6Im5pc2hhbnRrYXVzaGlrODIwNzRjaGFAZ21haWwuY29tIiwidGltZXN0YW1wIjoxNzE0Mjk1OTkxfQ.BIcEIi1fRO2EEfClBEWzLOdAcC7Z5HaMmB-n5UsnAUU"
            hdr1 = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
            if not bdetail:
                print(f"No course details found for user {userid}.")
                return
            bname = bdetail[0]["course_name"]
            
            couserid = []
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=156&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=156&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                for i in videodata:
                    couserid.append(i["id"])

            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=156&video_id={c}&ytflag=0&folder_wise_course=0"
                res4 = await fetch_data(session, url, headers=hdr1)
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
                except Exception as e:
                    print(f"Error processing video data: {e}")

            date = get_current_date()
            
            if date not in all_important:
                return await bot.send_message(chatid, text="🐇**कल् इस सब्जेक्ट मे कोई क्लास नही हुई**\n\n**आप आगे का रिवीजन कर लेना दोस्तो**❤️")

            data = all_important[date]
            title = data.get("title")
            video = data.get("download_link")
            pdf_1 = data.get("pdf_link")
            pdf_2 = data.get("pdf_link2")

            all_urls = ""
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
            await account_login(bot, all_urls, bname, chatid)
        
        except Exception as e:
            print(f"An error occurred: {e}")

scheduler.add_job(
    func=all_subject_send,
    trigger="cron",
    hour=12,
    minute=59,
    second=0, 
    args=[Client]
)

scheduler.start()
