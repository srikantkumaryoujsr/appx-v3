import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .. import bot as Client


# AUTH_USERS को इन-मैमोरी स्टोरेज के रूप में सेट करें
AUTH_USERS = set()

@Client.on_message(filters.command("manage_auth") & filters.user(AUTH_USERS))
async def manage_auth(bot, message):
    """Manage authorized users via buttons."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add User", callback_data="add_user"),
         InlineKeyboardButton("➖ Remove User", callback_data="remove_user")],
        [InlineKeyboardButton("📜 View Users", callback_data="view_users")]
    ])
    
    await message.reply_text(
        "Choose an action to manage authorized users:",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("add_user"))
async def add_user(bot, query: CallbackQuery):
    """Prompt for user ID to add."""
    await query.message.reply_text("Send the User ID you want to authorize:")
    
    user_response = await bot.listen(query.message.chat.id)
    try:
        user_id = int(user_response.text)
        if user_id in AUTH_USERS:
            await query.message.reply_text("This user is already authorized.")
        else:
            AUTH_USERS.add(user_id)
            await query.message.reply_text(f"User {user_id} has been added to AUTH_USERS.")
    except ValueError:
        await query.message.reply_text("Invalid User ID. Please provide a valid numeric User ID.")
    except Exception as e:
        await query.message.reply_text(f"Error: {e}")

@Client.on_callback_query(filters.regex("remove_user"))
async def remove_user(bot, query: CallbackQuery):
    """Prompt for user ID to remove."""
    if not AUTH_USERS:
        await query.message.reply_text("No users to remove.")
        return

    await query.message.reply_text("Send the User ID you want to remove:")
    
    user_response = await bot.listen(query.message.chat.id)
    try:
        user_id = int(user_response.text)
        if user_id in AUTH_USERS:
            AUTH_USERS.remove(user_id)
            await query.message.reply_text(f"User {user_id} has been removed from AUTH_USERS.")
        else:
            await query.message.reply_text("This user is not in the AUTH_USERS list.")
    except ValueError:
        await query.message.reply_text("Invalid User ID. Please provide a valid numeric User ID.")
    except Exception as e:
        await query.message.reply_text(f"Error: {e}")

@Client.on_callback_query(filters.regex("view_users"))
async def view_users(bot, query: CallbackQuery):
    """View all authorized users."""
    if not AUTH_USERS:
        await query.message.reply_text("No authorized users found.")
    else:
        users_list = "\n".join([f"- `{user}`" for user in AUTH_USERS])
        await query.message.reply_text(f"**Authorized Users:**\n\n{users_list}")

@Client.on_message(filters.command("AUTH"))
async def start(bot, message):
    await message.reply_text(
        "Hello! Use /manage_auth to manage authorized users (Admin only)."
    )
