import asyncio
import importlib
import logging
from pyrogram import idle
from plugins import bot as app
from plugins.modules import ALL_MODULES
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from datetime import datetime

# MongoDB सेटअप
mongo_client = MongoClient("mongodb+srv://sarkari226:Nzp4hfYpAdoo2dYH@cluster0.lavidof.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['course_database']  # MongoDB डेटाबेस नाम
courses_collection = db['courses']  # MongoDB कलेक्शन नाम

# Logging सेटअप
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Scheduler सेटअप
scheduler = AsyncIOScheduler()

async def _start():
    try:
        await app.start()
        LOGGER.info("Bot started.")
        await app.send_message(7224758848, "I am Alive")
        await schedule_all_courses()  # सभी कोर्स शेड्यूल करें
        await idle()
    except Exception as ex:
        LOGGER.error(f"Error starting bot: {ex}")
        quit(1)

async def add_course(subject_and_channel, chat_id, course_ids, hour, minute):
    course_data = {
        "subject_and_channel": subject_and_channel,
        "chat_id": chat_id,
        "course_ids": course_ids,
        "schedule": {"hour": hour, "minute": minute}
    }
    courses_collection.insert_one(course_data)  # MongoDB में डेटा जोड़ें
    LOGGER.info("Course added successfully.")
    schedule_course(subject_and_channel, chat_id, hour, minute)

def schedule_course(subject_and_channel, chat_id, hour, minute):
    """शेड्यूलर में कोर्स जोड़ें"""
    scheduler.add_job(
        func=all_subject_send,
        trigger=CronTrigger(hour=hour, minute=minute, second=0, timezone="Asia/Kolkata"),
        args=[subject_and_channel, chat_id]
    )
    LOGGER.info(f"Scheduled course for chat_id {chat_id} at {hour}:{minute}")

async def all_subject_send(subject_and_channel, chat_id):
    # यहाँ पर सभी सब्जेक्ट्स को भेजने का लॉजिक जोड़ा जाएगा
    LOGGER.info(f"Sending subjects for chat_id {chat_id} with data: {subject_and_channel}")

async def schedule_all_courses():
    all_courses = courses_collection.find()
    for course in all_courses:
        subject_and_channel = course['subject_and_channel']
        chat_id = course['chat_id']
        hour = course['schedule']['hour']
        minute = course['schedule']['minute']
        schedule_course(subject_and_channel, chat_id, hour, minute)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_start())
        scheduler.start()  # Scheduler को चालू करें
        loop.run_forever()
    finally:
        loop.close()
    LOGGER.info("Stopping bot")
