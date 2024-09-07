import asyncio, requests
import aiohttp
import base64,pytz
from pytz import utc
from datetime import datetime, time,timedelta

from pyrogram import  filters
from .. import bot as Client
from .. import bot
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from main import AUTH_USERS
from .download import account_login
AUTH_USERS.extend([6748451207, 6804421130, 6671207610, 6741261680])
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait

import pytz

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
    except ValueError as ve:
        pass
    except Exception as e:
        pass
    
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

async def all_subject_send(bot):
    subject_and_channel = {138: -1002344440579, 1029: -1002344440579, 1041: -1002344440579}
    
    try:
        start_message = await bot.send_message(chat_id=-1002344440579, text="**♻️𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫 𝐒𝐭𝐮𝐝𝐞𝐧𝐭𝐬...♻️**\n**𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞:- 𝐒𝐒𝐂 𝐆𝐃 𝟐𝟎𝟐𝟓 (अवसर बैच 𝟐.𝟎 )**\n**𝐂𝐥𝐚𝐬𝐬 𝐃𝐚𝐭𝐞** :- **{get_current_date()}**\n**नीचे इस तारीख की जितनी भी क्लासेस एप्लीकेशन पर हुई थी नीचे दी जा रही है👇👇👇👇**\n𝐘𝐨𝐮𝐫 𝐇𝐞𝐥𝐩𝐞𝐫 : 𝗠𝗥. 𝗛𝗔𝗖𝗞𝗘𝗥 🇮🇳")
        await bot.pin_chat_message(chat_id=-1002344440579, message_id=start_message.message_id)
    except Exception as e:
        print(f"Failed to send start message: {e}")
    
    for subjectid, chatid in subject_and_channel.items():
        try:
            await account_logins(bot, subjectid, chatid)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await account_logins(bot, subjectid, chatid)
        except Exception as e:
            print(f"Error processing subject {subjectid}: {e}")

    try:
        await bot.send_message(chat_id=-1002344440579, text=f"**♻️𝐒𝐭𝐮𝐝𝐞𝐧𝐭𝐬 𝐀𝐚𝐩𝐤𝐢 𝐂𝐥𝐚𝐬𝐬 𝐔𝐩𝐝𝐚𝐭𝐞 𝐊𝐚𝐫 𝐃𝐢 𝐠𝐚𝐢 𝐇𝐚𝐢 ♻️**\n**𝐃𝐚𝐭𝐞 : {get_current_date()}**\n\n**𝐑𝐞𝐚𝐜𝐭𝐢𝐨𝐧𝐬 ❤️ 𝐃𝐢𝐣𝐢𝐲𝐞**")
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid):
    userid ="3752241"
    async with aiohttp.ClientSession() as session:
        try:
            token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM3NTIyNDEiLCJlbWFpbCI6InNoYWtpdGt1bWFybndkODA1MTA0QGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcxNTI0NTYwNH0.AcUSabkEnTY0kXzNaSovcHPeNPmQWh5LMltyUnJJfoU"
            hdr1 = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'}
            
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
           
            bname=bdetail[0]["course_name"]
            # print(bdetail)
            
            
            all_urls = ""
            
            
            couserid=[]
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=157&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            # print(topic)
            
            topicids = [i["topicid"] for i in topic]
            
            
            
            videos=[]  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=157&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
                # print(all_important)
            for c in couserid:
                url=f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=157&video_id={c}&ytflag=0&folder_wise_course=0"
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
                    
                except Exception :
                    pass
                            
            #date="2024-05-31"
            date=get_current_date()
            data = all_important[date]
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
            await account_login(bot,all_urls,bname,chatid)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            # await m.reply(f"An error occurred. Please try again. {e}")
scheduler.add_job(
    func=all_subject_send,
     trigger="cron",
     hour=15,
     minute=32,
     second=0, 
     args=[Client]
)

scheduler.start()
