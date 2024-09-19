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
AUTH_USERS.extend([6748451207, 6804421130, 6671207610, 6741261680])
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait

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

def get_current_date_vsp():
    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    day_of_week = yesterday.strftime("%A").upper()  # Full weekday name
    month_name = yesterday.strftime("%B").upper()  # Full month name
    day = yesterday.strftime("%d").zfill(2)  # Day of the month
    year = yesterday.strftime("%Y")  # Year
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

@Client.on_message(filters.command("STARTRPF") & filters.user(AUTH_USERS))
async def start_subjects_command(bot, message):
    await all_subject_send(bot)

async def all_subject_send(bot):
    subject_and_channel = {828: -1002057819179, 829: -1002057819179, 830: -1002057819179, 831: -1002057819179, 832: -1002057819179, 833: -1002057819179, 917: -1002057819179, 935: -1002057819179, 958: -1002057819179, 1050: -1002057819179}
    
    try:
        start_message = await bot.send_message(
            chat_id=-1002057819179,
            text=f'**🔖{get_current_date_vsp()}:𝐔𝐩𝐝𝐚𝐭𝐞🔖**\n\n>**[📂]𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 ➤ RPF SI & CONSTABLE 2024( रेल रक्षक बैच )**\n\n 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐛𝐲 :➤ @ImTgHacker'
        )
        print(f"Message sent with ID: {start_message.id}")
        await asyncio.sleep(0.10)

        try:
            await bot.pin_chat_message(chat_id=-1002057819179, message_id=start_message.id)
            print("Message pinned successfully.")
        except Exception as e:
            print(f"Failed to pin message: {e}")
    
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
            chat_id=-1002057819179,
            text=f"**🔆𝐒𝐭𝐮𝐝𝐞𝐧𝐭𝐬 𝐀𝐚𝐩𝐤𝐢 𝐂𝐥𝐚𝐬𝐬{get_current_date_vsp()} 𝐔𝐩𝐝𝐚𝐭𝐞 𝐊𝐚𝐫 𝐃𝐢 𝐠𝐚𝐢 𝐇𝐚𝐢 🔆**\n\n**❤️𝐑𝐞𝐚𝐜𝐭𝐢𝐨𝐧𝐬 𝐝𝐨 𝐘𝐚𝐚𝐫❤️ **"
        )
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid):
    userid = "3752241"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjY2ODEzOTAiLCJlbWFpbCI6InByYWNoaXlhZGF2MTIzNEBnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MTQxODgwNDV9.Q9sHS33SjupDr0dvAnCjweKU2fdamClFBfFGg8hC66U"
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
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=156&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=156&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=156&video_id={c}&ytflag=0&folder_wise_course=0"
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
                            
            date=get_current_date()
            if date not in all_important:
                # Customize the message based on subjectid
                messages = {
                    828: f"Maths (RPF रक्षक बैच ) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    829: f"Reasoning (RPF रक्षक बैच )में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    830: f"Economics (RPF रक्षक बैच )में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    831: f"Geography (RPF रक्षक बैच )में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    832: f"History (RPF रक्षक बैच )में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    833: f" Physics (RPF रक्षक बैच )में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    917: f"Biology (RPF रक्षक बैच)में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    935: f"Static GK (RPF रक्षक बैच)में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    958: f"polity (RPF रक्षक बैच )में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1050: f"Chemistry (RPF रक्षक बैच)में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    # Add more subject IDs and their messages as needed
               }
                # Send the message if the subjectid is in the messages dictionary
                if subjectid in messages:
                    await bot.send_message(chatid, text=messages[subjectid])
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
            await account_login(bot, all_urls, bname, chatid)
        
        except Exception as e:
            print(f"An error occurred: {e}")

scheduler.add_job(
    func=all_subject_send,
    trigger="cron",
    hour=6,
    minute=30,
    second=0, 
    args=[Client]
)

scheduler.start()
