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
            [InlineKeyboardButton("🟢𝗔𝗗𝗗 𝗕𝗔𝗧𝗖𝗛➕❤️", callback_data="addbatch"),
             InlineKeyboardButton("🟢​𝗥𝗘𝗠𝗢𝗩𝗘 𝗕𝗔𝗧𝗖𝗛➖❤️", callback_data="removebatch")]
        ] + [
            [InlineKeyboardButton("🟢𝗩𝗜𝗘𝗪 𝗕𝗔𝗧𝗖𝗛𝗘𝗦👁️‍🗨️❤️", callback_data="viewbatches")]
        ] + [
            [InlineKeyboardButton("🟢𝗚𝗘𝗧 𝗔𝗟𝗟 𝗥𝗪𝗔 𝗕𝗔𝗧𝗖𝗛 𝗜𝗡𝗙𝗢.🦋", callback_data="get_all_courses")]
        ] + [
            [InlineKeyboardButton("👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 👨‍💻", url="https://t.me/rojgaarwithankit")]
        ])

        photo_url = "https://te.legra.ph/file/509795aa19e893839762d.jpg"

        caption = (
            "**🔵🟡🟢𝐇𝐞𝐥𝐥𝐨! 👋 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐛𝐨𝐭.🔵🟡🟢**\n\n"
            "**🔵🟡🟢𝐑𝐖𝐀 𝐃𝐀𝐈𝐋𝐘 𝐀𝐔𝐓𝐎 𝐔𝐏𝐃𝐀𝐓𝐄 𝐁𝐎𝐓🔵🟡🟢**\n\n"
            "**/RWA - 🔵🟡🟢𝐅𝐨𝐫 𝐑𝐰𝐚 𝐅𝐮𝐥𝐥 𝐓𝐱𝐭 𝐍𝐨 𝐍𝐞𝐞𝐝 𝐈𝐝 𝐏𝐚𝐬𝐬𝐬𝐰𝐨𝐫𝐝🔵🟡🟢 **\n\n"
            "**🔵🟡🟢𝐔𝐬𝐞 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐛𝐞𝐥𝐨𝐰 𝐭𝐨 𝐜𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐞 𝐨𝐫 𝐯𝐢𝐞𝐰 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐟𝐨𝐫 𝐞𝐚𝐜𝐡 𝐜𝐨𝐮𝐫𝐬𝐞. 😊🔵🟡🟢**\n\n"
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

    if data.startswith("addbatch"):
        course_num = data.replace("addbatch", "")
        await query.message.reply(
            f"Use the command `/addbatch` in the following format:\n"
            f"`/setconfig bname subjectid:chatid:threadid,... chat_id courseid hour minute`"
        )
    elif data.startswith("removebatch"):
        course_num = data.replace("removebatch", "")
        await query.message.reply(
            f"Fetching configuration for Course ... Use `/removebatch batch-Name` for details."
        )

    elif data.startswith("viewbatches"):
        course_num = data.replace("removebatch", "")
        await query.message.reply(
            f"Fetching configuration for Course ... Use `/viewbatches` for details."
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

                # Send results in chunks
                result = "\n\n".join(course_details)
                for chunk in [result[i:i+4000] for i in range(0, len(result), 4000)]:
                    await query.message.reply_text(chunk)

                await query.message.delete()

            except Exception as e:
                print(f"Error: {e}")
                await query.message.edit_text("An error occurred during the process. Please try again.")

    await query.answer()
