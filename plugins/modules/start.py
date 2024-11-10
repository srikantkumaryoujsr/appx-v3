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
            [InlineKeyboardButton("🟢𝗔𝗗𝗗 𝗕𝗔𝗧𝗖𝗛➕❤️", callback_data="addbatch")]
            
        ] + [InlineKeyboardButton("🟢​𝗥𝗘𝗠𝗢𝗩𝗘 𝗕𝗔𝗧𝗖𝗛➖❤️", callback_data="removebatch")]
        
        ] + [
            [InlineKeyboardButton("🟢𝗩𝗜𝗘𝗪 𝗕𝗔𝗧𝗖𝗛𝗘𝗦👁️‍🗨️❤️", callback_data="viewbatches")]
        ] + [
            [InlineKeyboardButton("🟢𝗚𝗘𝗧 𝗔𝗟𝗟 𝗥𝗪𝗔 𝗕𝗔𝗧𝗖𝗛 𝗜𝗡𝗙𝗢.🦋", callback_data="get_all_courses")]
        ] + [
            [InlineKeyboardButton("👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 👨‍💻", url="https://t.me/rojgaarwithankit")]
        ] + [
            [InlineKeyboardButton("❓ 𝐇𝐞𝐥𝐩 ❓", url="help")]
        ])

        photo_url = "https://te.legra.ph/file/509795aa19e893839762d.jpg"

        caption = (
            "**🔵🟡🟢ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʀᴏᴊɢᴀʀᴡɪᴛʜᴀɴᴋɪᴛ ᴄᴏᴀᴄʜɪɴɢ ʙᴏᴛ! 🎓 ᴛʜɪꜱ ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴘᴏꜱᴛꜱ ᴅᴀɪʟʏ ᴜᴘᴅᴀᴛᴇꜱ, ɪɴᴄʟᴜᴅɪɴɢ ᴄʟᴀꜱꜱᴇꜱ ᴀɴᴅ ɴᴏᴛᴇꜱ ꜰᴏʀ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴜʀꜱᴇꜱ. ꜱᴛᴀʏ ᴜᴘᴅᴀᴛᴇᴅ ᴡɪᴛʜ ᴛʜᴇ ʟᴀᴛᴇꜱᴛ ᴄᴏɴᴛᴇɴᴛ ᴇᴠᴇʀʏ ᴅᴀʏ!🔵🟡🟢**\n\n"
            "**🟢𝐈𝐦𝐩𝐨𝐫𝐭𝐚𝐧𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬🟢**\n"
            "**/RWA -❝​🇷​​🇴​​🇯​​🇬​​🇦​​🇷​​🇼​​🇮​​🇹​​🇭​​🇦​​🇳​​🇰​​🇮​​🇹​❝ ​🇦​​🇵​​🇵​ ​🇦​​🇳​​🇩​ ​🇩​​🇮​​🇸​​🇵​​🇱​​🇦​​🇾​ ​🇹​​🇭​​🇪​​🇲​ ​🇮​​🇳​ ​🇦​ ​🇹​​🇪​​🇽​​🇹​ ​🇫​​🇴​​🇷​​🇲​​🇦​​🇹​ ​🇼​​🇮​​🇹​​🇭​ ​🇨​​🇴​​🇲​​🇵​​🇱​​🇪​​🇹​​🇪​ ​🇱​​🇮​​🇳​​🇰​​🇸​**\n"
            "**/Help - ɢɪᴠᴇꜱ ᴀ ʟɪꜱᴛ ᴏꜰ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴛʜᴇɪʀ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴꜱ.​**\n\n"
            "**❤️"𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮 𝐟𝐨𝐫 𝐛𝐞𝐢𝐧𝐠 𝐩𝐚𝐫𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐥𝐞𝐚𝐫𝐧𝐢𝐧𝐠 𝐣𝐨𝐮𝐫𝐧𝐞𝐲 𝐰𝐢𝐭𝐡 𝐑𝐨𝐣𝐠𝐚𝐫𝐖𝐢𝐭𝐡𝐀𝐧𝐤𝐢𝐭! 𝐊𝐞𝐞𝐩 𝐮𝐩 𝐭𝐡𝐞 𝐠𝐫𝐞𝐚𝐭 𝐰𝐨𝐫𝐤, 𝐚𝐧𝐝 𝐝𝐨𝐧'𝐭 𝐡𝐞𝐬𝐢𝐭𝐚𝐭𝐞 𝐭𝐨 𝐫𝐞𝐚𝐜𝐡 𝐨𝐮𝐭 𝐚𝐧𝐲𝐭𝐢𝐦𝐞. 🚀"❤️**\n\n"
            "**🟢ᴘᴏᴡᴇʀᴇᴅ ʙʏ 🟡:- @rojgaarwithankit**"
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
        await query.message.edit_text("**ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ, ɪ’ᴍ ᴘʀᴇᴘᴀʀɪɴɢ ᴛʜᴇ ʙᴀᴛᴄʜ ᴅᴇᴛᴀɪʟꜱ ꜰᴏʀ ʏᴏᴜ. ɪᴛ ᴡɪʟʟ ᴏɴʟʏ ᴛᴀᴋᴇ ᴀʙᴏᴜᴛ 2 ᴍɪɴᴜᴛᴇꜱ!...**")

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

@Client.on_callback_query()
async def handle_callback(bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        help_text = (
            "**❝​🇼​​🇪​’​🇷​​🇪​ ​🇼​​🇴​​🇷​​🇰​​🇮​​🇳​​🇬​ ​🇴​​🇳​ ​🇦​ ​🇻​​🇮​​🇩​​🇪​​🇴​ ​🇹​​🇺​​🇹​​🇴​​🇷​​🇮​​🇦​​🇱​ ​🇹​​🇴​ ​🇲​​🇦​​🇰​​🇪​ ​🇺​​🇸​​🇮​​🇳​​🇬​ ​🇹​​🇭​​🇪​ ​🇧​​🇴​​🇹​ ​🇪​​🇻​​🇪​​🇳​ ​🇪​​🇦​​🇸​​🇮​​🇪​​🇷​❗ ​🇮​​🇹​ ​🇼​​🇮​​🇱​​🇱​ ​🇧​​🇪​ ​🇦​​🇻​​🇦​​🇮​​🇱​​🇦​​🇧​​🇱​​🇪​ ​🇸​​🇴​​🇴​​🇳​. ​🇰​​🇪​​🇪​​🇵​ ​🇱​​🇪​​🇦​​🇷​​🇳​​🇮​​🇳​​🇬​ ​🇼​​🇮​​🇹​​🇭​ ​🇺​​🇸​❗ 📹🚀❝**\n\n"
        )
        await query.message.edit_text(help_text)
