from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from .. import bot as Client

@Client.on_message(filters.command("start"))
async def start_message(bot, message):
    try:
        # Prepare buttons for multiple courses
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🟢​𝐒𝐄𝐓_𝐂𝐎𝐔𝐑𝐒𝐄 {i}​🔴", callback_data=f"setconfig{i}"),
             InlineKeyboardButton(f"🟢​𝐕𝐈𝐄𝐖_𝐂𝐎𝐔𝐑𝐒𝐄​ {i}🔴", callback_data=f"viewconfig{i}")]
            for i in range(1, 6)
        ] + [
            [InlineKeyboardButton("📚𝐆𝐞𝐭 𝐀𝐥𝐥 𝐑𝐰𝐚 𝐁𝐚𝐭𝐜𝐡 𝐈𝐧𝐟𝐨📚", callback_data="get_all_courses")]
        ] + [
            [InlineKeyboardButton("👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 👨‍💻", url="https://t.me/rojgaarwithankit")]
        ])
        
        # Photo URL or path (replace with your image path or URL)
        photo_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhvVXWRt7tfs0Y-PIpNOQlk8UbsT9DKyB8yNu7hHS2TGXeUKPnWPjaUF0Q-D4TUugqCFczMJOOpg89kapL8eGOG0FzjdjTZXym-1_xqKuqjaFUMQDTycUJfxNxjh6wWr0tTA_P5TgKvC9SVICeA3ksc8bHQlEpm7IhK5Cpzk4u6YV9xePnb2yB22hht/s1600/rojgar-with-ankit-app-installation.PNG"

        # Customize the message
        caption = (
            "**Hello! 👋 Welcome to the bot.**\n\n"
            "**RWA DAILY AUTO UPDATE BOT**\n\n"
            "**Use the buttons below to configure or view settings for each course. 😊**\n\n"
            "𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲 :- @rojgaarwithankit"
        )
        
        # Send the photo with the inline buttons
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
    await query.answer()
