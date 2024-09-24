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
AUTH_USERS.extend([6748451207])
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait
LOG_CHANNEL_ID = -1001801766701

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

@Client.on_message(filters.command("NTPCHD") & filters.user(AUTH_USERS))
async def start_subjects_command(bot, message):
    await all_subject_send(bot)

async def all_subject_send(bot):
    subject_and_channel = {1088: -1002003601367, 1090: -1002003601367, 1091: -1002003601367, 1092: -1002003601367, 1093: -1002003601367, 1094: -1002003601367}
    
    try:
        start_message = await bot.send_message(
            chat_id=-1002003601367,
            text=f'**☞{get_current_date_vsp()}:𝐔𝐩𝐝𝐚𝐭𝐞🔖**```\n☞𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 ➤ RRB NTPC 2024 गतिमान बैच 𝐋𝐢𝐯𝐞 🛑\n```🔅𝐐𝐮𝐚𝐥𝐢𝐭𝐲🔅:➤ 𝟕𝟐𝟎𝐩\n**☞🤡𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐛𝐲 :➤ @ImTgHacker**'
        )
        print(f"Message sent with ID: {start_message.id}")
        await asyncio.sleep(0.10)

        try:
            await bot.pin_chat_message(chat_id=-1002003601367, message_id=start_message.id)
            await bot.delete_messages(chat_id=-1002003601367, message_ids=[start_message.id + 1])
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
            chat_id=-1002003601367,
            text=f"**जिन बच्चों के पास इंटरनेट का अभाव या फिर वह मोबाइल इंटरनेट का उपयोग करते हैं तो आप काम क्वालिटी वाले चैनल से जुड़ सकते हैं 𝗤𝘂𝗮𝗹𝗶𝘁𝘆:- 𝟯𝟲𝟬𝗽😋 https://t.me/RWA_RRB_NTPC_GATIMAN_BATCH_2024 **"
        )
        await bot.send_message(
            chat_id=-1002003601367,
            text=f"**❤️ᴅᴇᴀʀ ꜱᴛᴜᴅᴇɴᴛ ᴀᴀᴘᴋɪ ᴄʟᴀꜱꜱ ᴜᴘᴅᴀᴛᴇ ʜᴏ ɢɪ ʜᴀɪ ❤️**\n\n**[ॐ] ᴅᴀᴛᴇ & ᴅᴀʏ : ➣ {get_current_date_vsp()}**\n\n**ʀᴇᴀᴄᴛɪᴏɴ इतना ज्यादा दो की ꜱᴇʟʟᴇʀ ʟᴏɢ की जल जाए बस 😁😁😁❤️💋**"
        )
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid):
    userid = "3752241"
    async with aiohttp.ClientSession() as session:
        try:
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjUxNzA3NyIsImVtYWlsIjoidml2ZWtrYXNhbmE0QGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcyNjU2MTM2Nn0.XimZ3jxS_j-7B4BpTUR9ZeeaJ8at-ROfPYMdm0GCf6I"
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
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=192&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid=192&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id=192&video_id={c}&ytflag=0&folder_wise_course=0"
                res4 = requests.get(url, headers=hdr1).json()
                video = res4.get("data", [])
                videos.append(video)
              
            for i in videos:
                try:
                    all_important[convert_timestamp_to_datetime(i["strtotime"])] = {
                        "title": i["Title"],
                        'pdf_link': decrypt_link(i['pdf_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link") else "",
                        'pdf_link2': decrypt_link(i['pdf_link2'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link2") else "",
                        'download_link': decrypt_link(i['download_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]).replace("720p", "720p") if i.get("download_link") else ""
                    }
                    
                except Exception:
                    pass
                            
            date=get_current_date()
            if date not in all_important:
                # Customize the message based on subjectid
                messages = {
                    1088: f"Maths (गतिमान बैच) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1090: f"Polity (रफ़्तार बैच + गतिमान बैच) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1091: f"History (रफ़्तार बैच + गतिमान बैच) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1092: f"Geography (रफ़्तार बैच + गतिमान बैच) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1093: f"Reasoning (गतिमान बैच) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
                    1094: f" Biology (गतिमान बैच) में {get_current_date_vsp()}```\nको या तो इस सब्जेक्ट में कल क्लास नहीं हुई थी या तो यह सब्जेक्ट में क्लासेस कंप्लीट हो गई है\n```",
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
    hour=4,
    minute=15,
    second=0, 
    args=[Client]
)

scheduler.start()
