import asyncio
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
    subject_and_channel = {848: -1002172298027, 849: -1002235512099, 850: -1002211669142, 851: -1002180965513,852: -1002161059509,853: -1002149612783,854: -1002166225417}
    # subject_and_channel = {848: "6741261680", 849:6741261680, 850:6741261680, 851:6741261680, 852:6741261680, 853:6741261680}
    for subjectid, chatid in subject_and_channel.items():
        try:
            await account_logins(bot,subjectid, chatid)
            # asyncio.sleep(180)
        except FloodWait as e:
            asyncio.sleep(e.value)
            await account_logins(bot,subjectid, chatid)
            
        


async def account_logins(bot,subjectid,chatid):
    userid ="1245678"
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
            
            
            
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=157&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            # print(topic)
            
            topicids = [i["topicid"] for i in topic]
            all_important = {}
                
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=157&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                # print(videodata)
                
                try:
                    for i in videodata:
                        all_important[convert_timestamp_to_datetime(i["strtotime"])] = {
                            "title": i["Title"],
                            'pdf_link': decrypt_link(i['pdf_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link") else "",
                            'pdf_link2': decrypt_link(i['pdf_link2'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link2") else "",
                            'download_link': decrypt_link(i['download_link']).replace("720p", "360p")
                        }
                except Exception as e:
                    print(e)
                # print(all_important)
            #date="2024-05-31"
            date=get_current_date()
            print(all_important.keys())
            print(date)
            if  date not in all_important.keys():
                
                return await bot.send_message(chatid,text="🐇दोस्तों कल इस विषय में कोई 𝐂𝐥𝐚𝐬𝐬 , नहीं हुई थी, आपलोग 𝐑𝐞𝐯𝐢𝐬𝐢𝐨𝐧 करिए❤️")

            data = all_important[date]
            title = data.get("title")
            all_urls = ""
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
     hour=12,
     minute=0,
     second=0, 
     args=[Client]
)

scheduler.start()
