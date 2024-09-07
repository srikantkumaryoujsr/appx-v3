import asyncio
import aiohttp
import base64
import pytz
from pytz import utc
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
    except (ValueError, KeyError) as e:
        pass
    except Exception as e:
        pass

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

async def all_subject_send(bot):
    subject_and_channel = {724: -1002344440579, 914: -1002344440579, 838: -1002344440579, 785: -1002344440579, 674: -1002344440579}
    # subject_and_channel = {828: "RPF_RWA", 829:6741261680, 830:6741261680, 831:6741261680, 833:6741261680, 917:6741261680}
        try:
            start_message = await bot.send_message(chat_id=-1002344440579, text="📢 Processing has started for the subjects!")
            await bot.pin_chat_message(chat_id=-1002344440579, message_id=start_message.message_id)
        except Exception as e:
            print(f"Failed to send start message: {e}")
    
    for subjectid, chatid in subject_and_channel.items():
        try:
            await account_logins(bot, subjectid, chatid)
        except FloodWait as e:
            await asyncio.sleep(1)
            await account_logins(bot, subjectid, chatid)

    # Send end message
    try:
        await bot.send_message(chat_id=-1002344440579, text=f"✅ Processing has completed for the subjects!\n\nDate :- **{get_current_date()}**")
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid):
    userid = "2717280"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjI3MTcyODAiLCJlbWFpbCI6Imt1bGRpcGtyaXNobmExQGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcxMzk0MDk3MH0.VhjdY81xSWilp_DuszLNkb79zWfo2tG8gVI_crR1lec"
            hdr1 = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
            bname = bdetail[0]["course_name"]
            
            couserid = []
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=126&subjectid={subjectid}&start=-1", headers=hdr1)
            topicids = [i["topicid"] for i in res3.get("data", [])]
            
            videos = []
            all_important = {}
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=126&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                except Exception as e:
                    print(e)
            
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=126&video_id={c}&ytflag=0&folder_wise_course=0"
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
                except Exception:
                    pass
            
            date = get_current_date()
            data = all_important.get(date, {})
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
     hour=11,
     minute=30,
     second=0, 
     args=[Client]
)

scheduler.start()
