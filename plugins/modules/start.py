import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .. import bot as Client


# Predefined token
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjUxNzA3NyIsImVtYWlsIjoidml2ZWtrYXNhbmE0QGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcyNjkzNzA4OX0.NM1SbOjDFZCLinFi66jKxwRQPgLWFN-_SAMgcPWvfk4"  # Replace this with your actual token

async def fetch_data(session, url, headers=None):
    """Fetch JSON data from a given URL."""
    async with session.get(url, headers=headers) as response:
        return await response.json()

@Client.on_message(filters.command("start"))
async def start_message(bot, message: Message):
    """Start message with multiple options."""
    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🟢​𝐒𝐄𝐓_𝐂𝐎𝐔𝐑𝐒𝐄 {i}​🔴", callback_data=f"setconfig{i}"),
             InlineKeyboardButton(f"🟢​𝐕𝐈𝐄𝐖_𝐂𝐎𝐔𝐑𝐒𝐄​ {i}🔴", callback_data=f"viewconfig{i}")] 
            for i in range(1, 6)
        ] + [
            [InlineKeyboardButton("📚𝐆𝐞𝐭 𝐀𝐥𝐥 𝐑𝐰𝐚 𝐁𝐚𝐭𝐜𝐡 𝐈𝐧𝐟𝐨📚", callback_data="get_all_courses")]
        ] + [
            [InlineKeyboardButton("👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 👨‍💻", url="https://t.me/rojgaarwithankit")]
        ])

        photo_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhvVXWRt7tfs0Y-PIpNOQlk8UbsT9DKyB8yNu7hHS2TGXeUKPnWPjaUF0Q-D4TUugqCFczMJOOpg89kapL8eGOG0FzjdjTZXym-1_xqKuqjaFUMQDTycUJfxNxjh6wWr0tTA_P5TgKvC9SVICeA3ksc8bHQlEpm7IhK5Cpzk4u6YV9xePnb2yB22hht/s1600/rojgar-with-ankit-app-installation.PNG"

        caption = (
            "**Hello! 👋 Welcome to the bot.**\n\n"
            "**RWA DAILY AUTO UPDATE BOT**\n\n"
            "**/manage_auth - Only OWNER Use This Command**\n\n"
            "**Use the buttons below to configure or view settings for each course. 😊**\n\n"
            "𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲 :- @rojgaarwithankit"
        )

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_url,
            caption=caption,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Failed to send start message: {e}")

@Client.on_callback_query()
async def handle_callback(bot, query: CallbackQuery):
    data = query.data

    if data.startswith("setconfig"):
        course_num = data.replace("setconfig", "")
        await query.message.reply(
            f"Use the command `/setconfig{course_num}` in the following format:\n"
            f"`/setconfig{course_num} subjectid:chatid:threadid,... chat_id courseid bname hour minute`"
        )
    elif data.startswith("viewconfig"):
        course_num = data.replace("viewconfig", "")
        await query.message.reply(
            f"Fetching configuration for Course {course_num}... Use `/viewconfig{course_num}` for details."
        )
    elif data == "get_all_courses":    
        await query.message.edit_text("सेवा में श्रीमान or श्रीमती हमको बैच डीटेल्स देने में थोड़ा समय लगेगा एक-दो मिनट का तब तक आप इंतजार करिए..... धन्यवाद 😜")

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
                    return await query.message.edit_text("No courses found for this account.")

                # Prepare course and subject details with batch information
                course_details = []
                for course in courses:
                    course_id = course.get("id")
                    course_name = course.get("course_name")

                    # Fetch subjects and batch details under each course
                    subjects_response = await fetch_data(
                        session, 
                        f"https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid={course_id}&start=-1", 
                        headers=headers
                    )
                    subjects = subjects_response.get("data", [])
                    
                    # Fetch batch details for each course
                    batch_response = await fetch_data(
                        session, 
                        f"https://rozgarapinew.teachx.in/get/allbatch?courseid={course_id}", 
                        headers=headers
                    )
                    batches = batch_response.get("data", [])

                    subjects_info = "\n".join([f"   - {subj['subjectid']}: {subj['subject_name']}" for subj in subjects])

                    # Prepare batch info
                    batch_info = "\n".join([
                        f"   - Batch Name: {batch['batch_name']}\n"
                        f"     Start Date: {batch['start_date']}\n"
                        f"     End Date: {batch['end_date']}\n"
                        f"     Subscription Status: {'Active' if batch['is_active'] else 'Inactive'}"
                        for batch in batches
                    ])

                    course_info = f"**Course ID**: `{course_id}`\n**Course Name**: {course_name}\n**Subjects**:\n{subjects_info}\n**Batches**:\n{batch_info}\n"
                    course_details.append(course_info)

                # Send results in chunks
                result = "\n\n".join(course_details)
                for chunk in [result[i:i+4000] for i in range(0, len(result), 4000)]:
                    await query.message.reply_text(chunk)

                await query.message.delete()

            except Exception as e:
                print(f"Error: {e}")
                await query.message.edit_text("An error occurred during the process. Please try again.")

    await query.answer()
