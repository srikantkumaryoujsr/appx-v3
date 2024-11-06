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
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.errors import FloodWait
LOG_CHANNEL_ID = -1002004338182
import json
import os

# File to store configuration
CONFIG_FILE = "config4.json"

# Load configuration from file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

# Save configuration to file
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

# Initialize configuration
config = load_config()
subject_and_channel = config.get("subject_and_channel", {})
chat_id = config.get("chat_id", -1002289423851)
courseids = config.get("courseids", 204)
scheduler_time = config.get("scheduler_time", {"hour": 0, "minute": 0})

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

@Client.on_message(filters.command("startnow4") & filters.user(AUTH_USERS))
async def start_subjects_command(bot, message):
    await all_subject_send(bot)

async def all_subject_send(bot):
    for subjectid, (chatid, message_thread_id) in subject_and_channel.items():
        try:
            await account_logins(bot, subjectid, chatid, message_thread_id)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await account_logins(bot, subjectid, chatid, message_thread_id)
        except Exception as e:
            print(f"Error processing subject {subjectid}: {e}")

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=f"**❤️ᴅᴇᴀʀ ꜱᴛᴜᴅᴇɴᴛ ᴀᴀᴘᴋɪ ᴄʟᴀꜱꜱ ᴜᴘᴅᴀᴛᴇ ʜᴏ ɢɪ ʜᴀɪ ❤️**\n\n**[ॐ] ᴅᴀᴛᴇ & ᴅᴀʏ : ➣ {get_current_date_vsp()}**\n\n**ʀᴇᴀᴄᴛɪᴏɴ❤️**", message_thread_id = 1
        )
    except Exception as e:
        print(f"Failed to send end message: {e}")

async def account_logins(bot, subjectid, chatid, message_thread_id):
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
            res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid={courseids}&subjectid={subjectid}&start=-1", headers=hdr1)
            topic = res3.get("data", [])
            
            topicids = [i["topicid"] for i in topic]
            
            videos = []  
            all_important = {}  
            all_urls = ""
            for t in topicids:
                url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid={courseids}&subjectid={subjectid}&topicid={t}&start=-1&conceptid="
                
                res4 = await fetch_data(session, url, headers=hdr1)
                videodata = res4.get("data", [])
                
                try:
                    for i in videodata:
                        couserid.append(i["id"])
                        
                except Exception as e:
                    print(e)
            for c in couserid:
                url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id={courseids}&video_id={c}&ytflag=0&folder_wise_course=0"
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
@Client.on_message(filters.command("setconfig4") & filters.user(AUTH_USERS))
async def set_config(bot, message):
    global subject_and_channel, chat_id, courseid, bname  # Declare global variables at the beginning
    
    try:
        # Split the command into parts, expecting 7 parts after the command
        parts = message.text.split(" ", 6)  # Allow 7 parts: command + 6 params (updated)
        print("Split parts:", parts)  # Debug log
        
        # Check if we have the expected number of parts
        if len(parts) != 7:
            await message.reply("Error: Invalid command format. Expected format is:\n"
                                "`/setconfig4 subject_and_channel chat_id courseid bname hour minute`")
            return
        
        # Parse the subject_and_channel part
        new_subject_and_channel = {}
        subject_channel_pairs = parts[1].split(",")  # Split by commas for each subject-channel pair
        print("Subject and Channel Pairs:", subject_channel_pairs)  # Debug log
        
        for pair in subject_channel_pairs:
            subject_id, chat_id, thread_id = map(int, pair.split(":"))  # Split each pair by colon and convert to int
            new_subject_and_channel[subject_id] = (chat_id, thread_id)  # Add to dictionary as (chat_id, thread_id)
        
        # Parse remaining parts
        new_chat_id = int(parts[2])
        new_courseid = int(parts[3])
        new_bname = parts[4]  # New bname (course name) input
        new_hour = int(parts[5])
        new_minute = int(parts[6])

        # Update the global variables
        subject_and_channel = new_subject_and_channel
        chat_id = new_chat_id
        courseid = new_courseid
        bname = new_bname  # Update bname

        # Save configuration for persistence
        config_data = {
            "subject_and_channel": subject_and_channel,
            "chat_id": chat_id,
            "courseid": courseid,
            "bname": bname,  # Save bname
            "scheduler_time": {"hour": new_hour, "minute": new_minute}
        }
        save_config(config_data)

        # Reschedule the job with updated time
        scheduler.remove_all_jobs()
        scheduler.add_job(
            func=all_subject_send,
            trigger=CronTrigger(hour=new_hour, minute=new_minute, second=0, timezone="Asia/Kolkata"),
            args=[bot]
        )

        await message.reply(f"**𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧🦋🎉🎊vsp4 𝐮𝐩𝐝𝐚𝐭𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲**:\n\n"
                            f"**🟢ꜱᴜʙᴊᴇᴄᴛꜱ ᴀɴᴅ ᴄʜᴀɴɴᴇʟꜱ🟡**: `{subject_and_channel}`\n"
                            f"**🟢ɢʀᴏᴜᴘ ᴄʜᴀᴛ ɪᴅ🟡**: `{chat_id}`\n"
                            f"**🟢ᴄᴏᴜʀꜱᴇ ɪᴅ🟡**: `{courseid}`\n"
                            f"**🟢ᴄᴏᴜʀꜱᴇ ɴᴀᴍᴇ🟡**: `{bname}`\n"  # Display bname
                            f"**🟢ꜱᴄʜᴇᴅᴜʟᴇᴅ ᴛɪᴍᴇ🟡**: `{new_hour}`:`{new_minute}` IST")

    except ValueError as e:
        await message.reply(f"Error updating configuration: Invalid format or type: {e}")
    except Exception as e:
        await message.reply(f"Error updating configuration: {e}")

@Client.on_message(filters.command("viewconfig4") & filters.user(AUTH_USERS))
async def view_config(bot, message):
    try:
        # Load the current configuration from the file for display
        config = load_config()
        
        # Extract configuration details
        subject_and_channel = config.get("subject_and_channel", {})
        chat_id = config.get("chat_id", -1002289423851)
        courseid = config.get("courseid", 204)
        bname = config.get("bname", "N/A")  # Provide a default in case it's not set
        scheduler_time = config.get("scheduler_time", {"hour": 0, "minute": 0})
        
        # Prepare the configuration message
        config_message = (
            f"**Current Configuration**:\n\n"
            f"**🟢 Subjects and Channels**: `{subject_and_channel}`\n"
            f"**🟢 Group Chat ID**: `{chat_id}`\n"
            f"**🟢 Course ID**: `{courseid}`\n"
            f"**🟢 Course Name**: `{bname}`\n"
            f"**🟢 Scheduled Time**: `{scheduler_time['hour']}`:`{scheduler_time['minute']}` IST"
        )
        
        # Send the configuration details to the user
        await message.reply(config_message)
    except Exception as e:
        await message.reply(f"Error retrieving configuration: {e}")

# Start scheduler
scheduler.start()
