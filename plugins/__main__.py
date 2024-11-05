# @sarkari_student
import asyncio
import importlib
from pyrogram import idle
from plugins import LOGGER, bot as app
from plugins.modules import ALL_MODULES
from pymongo import MongoClient

# MongoDB सेटअप
mongo_client = MongoClient("mongodb+srv://sarkari226:Nzp4hfYpAdoo2dYH@cluster0.lavidof.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['course_database']  # MongoDB डेटाबेस नाम
courses_collection = db['courses']  # MongoDB कलेक्शन नाम

async def _start():
    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)
    
    for all_module in ALL_MODULES:
        importlib.import_module("plugins.modules." + all_module)

    LOGGER.info(f"@{app.username} Started.")
    await app.send_message(7224758848, "I am Alive")
    await idle()

# कोर्स जोड़ने का फ़ंक्शन
async def add_course(subject_and_channel, chat_id, course_ids, hour, minute):
    course_data = {
        "subject_and_channel": subject_and_channel,
        "chat_id": chat_id,
        "course_ids": course_ids,
        "schedule": {"hour": hour, "minute": minute}
    }
    courses_collection.insert_one(course_data)  # MongoDB में डेटा जोड़ें
    LOGGER.info("Course added successfully.")

# सभी कोर्स शेड्यूल करें
async def schedule_all_courses():
    all_courses = courses_collection.find()
    for course in all_courses:
        subject_and_channel = course['subject_and_channel']
        chat_id = course['chat_id']
        hour = course['schedule']['hour']
        minute = course['schedule']['minute']
        # यहाँ कोर्स के शेड्यूलिंग के लिए लॉजिक जोड़ें
        # जैसे कि पहले से दिए गए कोड में all_subject_send को कॉल करें

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_start())
    finally:
        loop.close()
    LOGGER.info("Stopping bot")
