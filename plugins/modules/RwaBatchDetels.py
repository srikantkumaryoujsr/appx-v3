import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Define your token here
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjUxNzA3NyIsImVtYWlsIjoidml2ZWtrYXNhbmE0QGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcyNjkzNzA4OX0.NM1SbOjDFZCLinFi66jKxwRQPgLWFN-_SAMgcPWvfk4"  # Replace this with your actual token

async def fetch_data(session, url, headers=None):
    """Fetch JSON data from a given URL."""
    async with session.get(url, headers=headers) as response:
        return await response.json()

@Client.on_callback_query(filters.regex("get_all_courses"))
async def get_all_courses_info(bot: Client, callback_query):
    """Fetch all course and subject details using predefined token."""
    await m.reply_text("𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐚𝐥𝐥 𝐜𝐨𝐮𝐫𝐬𝐞 𝐝𝐞𝐭𝐚𝐢𝐥𝐬...𝟐,𝟑 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐖𝐚𝐢𝐭 😂")

    headers = {
        'auth-key': 'appxapi',
        'authorization': TOKEN,
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Fetch all courses
            courses_response = await fetch_data(session, "https://rozgarapinew.teachx.in/get/mycourse?userid=0", headers=headers)
            courses = courses_response.get("data", [])
            
            if not courses:
                return await m.reply_text("No courses found for this account.")
            
            # Prepare course and subject details
            course_details = []
            for course in courses:
                course_id = course.get("id")
                course_name = course.get("course_name")
                
                # Fetch subjects under each course
                subjects_response = await fetch_data(
                    session, 
                    f"https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid={course_id}&start=-1", 
                    headers=headers
                )
                
                subjects = subjects_response.get("data", [])
                subjects_info = "\n".join([f"   - {subj['subjectid']}: {subj['subject_name']}" for subj in subjects])
                
                course_info = f"**Course ID**: `{course_id}`\n**Course Name**: {course_name}\n**Subjects**:\n{subjects_info}\n"
                course_details.append(course_info)
            
            # Split messages if content exceeds Telegram limits
            result = "\n\n".join(course_details)
            for chunk in [result[i:i+4000] for i in range(0, len(result), 4000)]:
                await m.reply_text(chunk)
        
        except Exception as e:
            print(f"Error: {e}")
            await m.reply_text("An error occurred during the process. Please try again.")
