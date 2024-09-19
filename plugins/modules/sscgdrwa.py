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
from pyrogram.errors import FloodWait

AUTH_USERS.extend([6748451207, 6804421130, 6671207610, 6741261680])

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

def get_current_date():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def convert_timestamp_to_datetime(timestamp: int) -> str:
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

def get_current_date_vsp():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    return f"{yesterday.strftime('%d')}-{yesterday.strftime('%B').upper()}-{yesterday.strftime('%Y')}, {yesterday.strftime('%A').upper()}"

async def fetch_data(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

def decrypt_link(link):
    try:
        decoded_link = base64.b64decode(link)
        key = b'638udh3829162018'
        iv = b'fedcba9876543210'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(decoded_link), AES.block_size).decode('utf-8')
    except Exception:
        pass

async def all_subject_send(bot):
    subject_and_channel = {138: -1001999613479, 1076: -1001999613479, 1077: -1001999613479, 1078: -1001999613479, 1079: -1001999613479, 1080: -1001999613479, 1081: -1001999613479, 1082: -1001999613479}
    
    try:
        start_message = await bot.send_message(
            chat_id=-1001999613479,
            text=f'**☞{get_current_date_vsp()}:𝐔𝐩𝐝𝐚𝐭𝐞🔖**\n\n**☞𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 ➤ 𝐒𝐒𝐂 𝐆𝐃 𝟐𝟎𝟐𝟓 ( अवसर बैच 𝟐.𝟎 ) 𝐋𝐢𝐯𝐞 🛑**\n\n**☞𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐛𝐲 :➤ @ImTgHacker**'
        )
        await asyncio.sleep(0.10)
        await bot.pin_chat_message(chat_id=-1001999613479, message_id=start_message.id)
    
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
        await bot.send_message(
            chat_id=-1001999613479,
            text=f"**🔆𝐒𝐭𝐮𝐝𝐞𝐧𝐭𝐬 𝐀𝐚𝐩𝐤𝐢 𝐂𝐥𝐚𝐬𝐬{get_current_date_vsp()}**\n**𝐔𝐩𝐝𝐚𝐭𝐞 𝐊𝐚𝐫 𝐃𝐢 𝐠𝐚𝐢 𝐇𝐚𝐢 🔆**\n\n**❤️𝐑𝐞𝐚𝐜𝐭𝐢𝐨𝐧𝐬 𝐝𝐨 𝐘𝐚𝐚𝐫❤️ **"
        )
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid):
    userid = "3752241"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM3NTIyNDEiLCJlbWFpbCI6InNoYWtpdGt1bWFybndkODA1MTA0QGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcxNTI0NTYwNH0.AcUSabkEnTY0kXzNaSovcHPeNPmQWh5LMltyUnJJfoU"
            hdr1 = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
            bname = bdetail[0]["course_name"]
            all_urls = ""
            couserid = []
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=188&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            topicids = [i["topicid"] for i in topic]
            videos = []  
            all_important = {}  

            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=188&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                for i in videodata:
                    couserid.append(i["id"])
                    
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=188&video_id={c}&ytflag=0&folder_wise_course=0"
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
                messages = {
                    138: f"Current Affairs में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1076: f"Maths (अवसर2.O) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1077: f"English (अवसर बैच 2.O) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1078: f"Hindi (अवसर बैच 2.0) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1079: f"Geography (अवसर बैच 2.0) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1080: f"Reasoning (अवसर बैच 2.0) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1081: f"Polity (अवसर बैच 2.0) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1082: f"Physics(अवसर बैच 2.0) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                }
                if subjectid in messages:
                    await bot.send_message(chatid, text=messages[subjectid])
                return

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
            await account_login(bot, all_urls, bname, chatid)
        
        except Exception as e:
            print(f"An error occurred: {e}")

#@scheduler.scheduled_job('cron', id='all_subject_send_job', hour=6, minute=1, second=0)
#async def scheduled_task():
    #await all_subject_send(Client)

@Client.on_message(filters.command("set_time"))
async def set_time(client, message):
    await message.reply("Kripya apna desired time (HH:MM:SS) format me dein.")
    
    response_message = await client.get_next_message(chat_id=message.chat.id)
    
    try:
        time_str = response_message.text
        hour, minute, second = map(int, time_str.split(':'))
        
        scheduler.reschedule_job(
            'all_subject_send_job',
            trigger='cron',
            hour=hour,
            minute=minute,
            second=second
        )
        
        await message.reply(f"Scheduler time update ho gaya hai: {time_str}.")
    except Exception:
        await message.reply("Koi galti hui, kripya sahi format me time dein (HH:MM:SS).")

scheduler.add_job(
    func=all_subject_send,
    trigger="cron",
    hour=6,
    minute=1,
    second=0
)

scheduler.start()
