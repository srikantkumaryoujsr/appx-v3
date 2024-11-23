import aiohttp
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .. import bot as Client
from plugins.modules.subscription import check_subscription


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
            [InlineKeyboardButton("🟢𝗔𝗗𝗗 𝗕𝗔𝗧𝗖𝗛➕❤️", callback_data="addbatch")],
            [InlineKeyboardButton("🟢​𝗥𝗘𝗠𝗢𝗩𝗘 𝗕𝗔𝗧𝗖𝗛➖❤️", callback_data="removebatch")],
            [InlineKeyboardButton("🟢𝗩𝗜𝗘𝗪 𝗕𝗔𝗧𝗖𝗛𝗘𝗦👁️‍🗨️❤️", callback_data="viewbatches")],
            [InlineKeyboardButton("🟢𝗚𝗘𝗧 𝗔𝗟𝗟 𝗥𝗪𝗔 𝗕𝗔𝗧𝗖𝗛 𝗜𝗡𝗙𝗢.🦋", callback_data="get_all_courses")],
            [InlineKeyboardButton("👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 👨‍💻", url="https://t.me/Berojgaarwithankit")],
            [InlineKeyboardButton("❓ 𝐇𝐞𝐥𝐩 ❓", callback_data="help")]
        ])

        photo_url = "https://te.legra.ph/file/509795aa19e893839762d.jpg"

        caption = (
            "**🔵🟡🟢ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʀᴏᴊɢᴀʀᴡɪᴛʜᴀɴᴋɪᴛ ᴄᴏᴀᴄʜɪɴɢ ʙᴏᴛ! 🎓 ᴛʜɪꜱ ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴘᴏꜱᴛꜱ ᴅᴀɪʟʏ ᴜᴘᴅᴀᴛᴇꜱ- ɪɴᴄʟᴜᴅɪɴɢ ᴄʟᴀꜱꜱᴇꜱ ᴀɴᴅ ɴᴏᴛᴇꜱ ꜰᴏʀ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴜʀꜱᴇꜱ. ꜱᴛᴀʏ ᴜᴘᴅᴀᴛᴇᴅ ᴡɪᴛʜ ᴛʜᴇ ʟᴀᴛᴇꜱᴛ ᴄᴏɴᴛᴇɴᴛ ᴇᴠᴇʀʏ ᴅᴀʏ!🔵🟡🟢**\n\n"
            "**❤️𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮 𝐟𝐨𝐫 𝐛𝐞𝐢𝐧𝐠 𝐩𝐚𝐫𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐥𝐞𝐚𝐫𝐧𝐢𝐧𝐠 𝐣𝐨𝐮𝐫𝐧𝐞𝐲 𝐰𝐢𝐭𝐡 𝐑𝐨𝐣𝐠𝐚𝐫𝐖𝐢𝐭𝐡𝐀𝐧𝐤𝐢𝐭! 𝐊𝐞𝐞𝐩 𝐮𝐩 𝐭𝐡𝐞 𝐠𝐫𝐞𝐚𝐭 𝐰𝐨𝐫𝐤, 𝐚𝐧𝐝 𝐝𝐨𝐧'𝐭 𝐡𝐞𝐬𝐢𝐭𝐚𝐭𝐞 𝐭𝐨 𝐫𝐞𝐚𝐜𝐡 𝐨𝐮𝐭 𝐚𝐧𝐲𝐭𝐢𝐦𝐞. 🚀❤️**\n\n"
            "**🟢ᴘᴏᴡᴇʀᴇᴅ ʙʏ 🟡:- @Berojgaarwithankit**"
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
        if not check_subscription(query.from_user.id):
                await query.answer("❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴", show_alert=True)
                return
            
        await query.message.reply(
            f"**🟢🔵🟡 ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ🟠☢️ :-**\n\n`/setconfig bname subjectid:chatid:threadid,... chat_id courseid hour minute`"
        )
    elif data.startswith("removebatch"):
        if not check_subscription(query.from_user.id):
                await query.answer("❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴", show_alert=True)
                return
            
        await query.message.reply(
            f"**🟢🔵🟡 ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ🟠☢️ :-**\n\n `/removebatch batch-Name`"
        )

    elif data.startswith("viewbatches"):
        if not check_subscription(query.from_user.id):
                await query.answer("❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴", show_alert=True)
                return
            
        await query.message.reply(
            f"**🟢🔵🟡 ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ🟠☢️ :-**\n\n `/viewbatches`"
        )
    elif data.startswith("help"):
        await query.message.reply(
            f"**ᴡᴇ’ʀᴇ ᴡᴏʀᴋɪɴɢ ᴏɴ ᴀ ᴠɪᴅᴇᴏ ᴛᴜᴛᴏʀɪᴀʟ ᴛᴏ ᴍᴀᴋᴇ ᴜꜱɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴇᴠᴇɴ ᴇᴀꜱɪᴇʀ! ɪᴛ ᴡɪʟʟ ʙᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ꜱᴏᴏɴ. ᴋᴇᴇᴘ ʟᴇᴀʀɴɪɴɢ ᴡɪᴛʜ ᴜꜱ! 📹🚀**"
        )
    elif data == "get_all_courses":
        if not check_subscription(query.from_user.id):
                await query.answer("❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴", show_alert=True)
                return
            
        await query.message.reply_text("**ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ, ɪ’ᴍ ᴘʀᴇᴘᴀʀɪɴɢ ᴛʜᴇ ʙᴀᴛᴄʜ ᴅᴇᴛᴀɪʟꜱ ꜰᴏʀ ʏᴏᴜ. ɪᴛ ᴡɪʟʟ ᴏɴʟʏ ᴛᴀᴋᴇ ᴀʙᴏᴜᴛ 2 ᴍɪɴᴜᴛᴇꜱ!...**")
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

                # Send details for each course
                for course in courses:
                    course_id = course.get("id")
                    course_name = course.get("course_name")

                    # Fetch subjects under the course
                    subjects_response = await fetch_data(
                        session,
                        f"https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid={course_id}&start=-1",
                        headers=headers
                    )

                    subjects = subjects_response.get("data", [])
                    subjects_info = "\n".join([f"`{subj['subjectid']}`: `{subj['subject_name']}`" for subj in subjects]) if subjects else "No subjects found."

                    # Send course info
                    course_info = (
                        f"**Course ID**: `{course_id}`\n"
                        f"**Course Name**: `{course_name}`\n"
                        f"**Subjects**:\n`{subjects_info}`\n"
                    )
                    await query.message.reply_text(course_info)

                await query.message.delete()

            except Exception as e:
                print(f"Error fetching courses: {e}")
                await query.message.edit_text("An error occurred. Please try again.")

        await query.answer()

@Client.on_message(filters.command("creat"))
async def create_topics(bot, message: Message):
    if not check_subscription(message.from_user.id):
        await message.reply_text("**❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴**\n\n**🟡☢️ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ꜱᴜʙꜱᴄʀɪʙᴇ.🔵❤️**")
        return
    """Creates topics in a specified group chat."""
    try:
        # Split input by lines
        lines = message.text.strip().splitlines()

        # Debug: Show each line of the input
        print("Input lines:")
        for line in lines:
            print(line)

        # Parse chat_id from the first line
        chat_id_line = lines[0]
        chat_id_match = re.search(r"-\d+", chat_id_line)
        if not chat_id_match:
            await message.reply_text("Invalid chat ID format.")
            return

        chat_id = int(chat_id_match.group())  # Extract chat ID as integer

        # Extract topics (ID and name) from the remaining lines
        topics = []
        for line in lines[1:]:
            # Adjusted regex to match without the leading hyphen
            match = re.search(r"(\d+): (.+)", line)
            if match:
                topic_id = int(match.group(1))
                topic_name = match.group(2).strip(" @")  # Remove trailing "@" or whitespace
                topics.append((topic_id, topic_name))

        # Debug: Show the parsed topics
        print(f"Parsed Topics: {topics}")

        # If no topics were parsed
        if not topics:
            await message.reply_text("No topics found in the provided input.")
            return

        # List to store created topics in the required format
        created_topics = []
        topic_counter = 3  # Start from topic number 3

        # Create each topic in the specified chat
        for topic_id, topic_name in topics:
            try:
                # Attempt to create the forum topic using the correct 'title' argument
                result = await bot.create_forum_topic(chat_id=chat_id, title=topic_name)
                print(f"Created topic: {topic_name} (ID: {topic_id})")  # Debug output
                
                # Add to the list of created topics with the sequential number starting from 3
                created_topics.append(f"{topic_id}:{chat_id}:{topic_counter}")
                topic_counter += 1  # Increment the counter for the next topic

                await message.reply_text(f"Topic '{topic_name}' (ID: {topic_id}) created successfully.")
            except Exception as e:
                print(f"Error creating topic: {topic_name} (ID: {topic_id}) - {e}")  # Debug output
                await message.reply_text(f"Failed to create topic '{topic_name}' (ID: {topic_id}): {e}")
        
        # If any topics were created, send the summary message
        if created_topics:
            # Join the created topics into the specified format
            summary_message = ",".join(created_topics)
            await message.reply_text(f"Created topics: `{summary_message}`")
    
    except Exception as e:
        print(f"Error: {e}")  # Debug output for any errors
        await message.reply_text(f"An error occurred: {e}")
