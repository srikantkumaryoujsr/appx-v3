import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
from dotenv import load_dotenv
from .. import bot as Client
import re

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://heeokumailseptember:nfOkF8F4zn1FIAFQ@cluster0.xb62l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['telegram_bot']
collection = db['channels_groups']

# Owner ID (Owner who will receive gift card messages)
OWNER_ID = "7224758848"

# Temporary storage for user selected channels and pending approvals
pending_approvals = {}

# Bot start command handler
@Client.on_message(filters.command("startvsp"))
async def start_message(bot, message: Message):
    """Start command handler to show welcome message and channel buttons."""
    try:
        logger.info(f"User {message.from_user.id} initiated start command.")
        entries = list(collection.find().limit(5))
        buttons = [
            [InlineKeyboardButton(entry['name'], callback_data=f"link_{entry['chat_id']}")]
            for entry in entries
        ]

        # Add 'Add Channel' and 'Remove Channel' buttons at the bottom
        buttons.append([InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")])
        buttons.append([InlineKeyboardButton("➖ Remove Channel", callback_data="remove_channel")])

        # If there are more than 5 channels, add a 'Next Page' button
        if collection.count_documents({}) > 5:
            buttons.append([InlineKeyboardButton("➡️ Next Page", callback_data="next_page_1")])

        # Send welcome photo, caption, and channel buttons
        await bot.send_photo(
            chat_id=message.chat.id,
            photo="https://te.legra.ph/file/509795aa19e893839762d.jpg",
            caption="**स्वागत है आपका हमारे टेलीग्राम बोट में, जो की premium channel और Groups का लिंक प्रोवाइड कराता है।**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        logger.info(f"Sent welcome message to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Error in start_message: {e}")
        await message.reply("An error occurred while fetching channels/groups.")

# Callback handler for channel buttons
@Client.on_callback_query(filters.regex(r"^link_"))
async def handle_channel_selection(bot, query: CallbackQuery):
    """Send gift card request for selected channel."""
    chat_id = query.data.split("_")[1]
    try:
        logger.info(f"User {query.from_user.id} selected channel {chat_id}.")
        chat = await bot.get_chat(chat_id)
        pending_approvals[query.from_user.id] = chat_id  # Store selected channel for user

        await query.message.reply(
            f"**{chat.title}** चैनल में जुड़ने के लिए:\n\n"
            "फोन पर गिफ्ट कार्ड नंबर और गिफ्ट कार्ड पिन भेजें।\n\n"
            "**Example:**\n"
            "Gift Card Number: 9092411066032820\n"
            "Gift Card Pin: 651993"
        )
    except Exception as e:
        logger.error(f"Error in handle_channel_selection: {e}")
        await query.message.reply("An error occurred while processing your request.")
    await query.answer()

# Gift card message handler
# Gift card message handler (Only active after channel selection)
async def handle_gift_card(bot, message: Message):
    """Forward gift card message to the owner for approval."""
    
    # Only handle gift card messages if the user has selected a channel
    user_id = message.from_user.id
    if user_id in user_state and "channel" in user_state[user_id]:  # Check if the user is in "gift card input mode"
        # Check if the message starts with "/gift"
        if message.text.startswith("/gift"):
            # Extract the card number and card pin from the message text
            try:
                # Strip the '/gift' command and split the rest into card number and pin
                _, card_number, card_pin = message.text.split()

                # Ensure both card number and card pin are of the correct length
                if len(card_number) == 16 and len(card_pin) == 6:
                    chat_id = user_state[user_id]["channel"]  # Get the selected channel's chat_id
                    
                    logger.info(f"Forwarding gift card from user {user_id} for channel {chat_id}.")
                    
                    # Forward the gift card message to the owner
                    await bot.send_message(
                        OWNER_ID,
                        f"Gift card received from {message.from_user.mention}:\n\n"
                        f"Gift Card Number: {card_number}\nGift Card Pin: {card_pin}\n\n"
                        f"Channel requested: {chat_id}"
                    )
                    
                    # Inform the user
                    await message.reply("आपका गिफ्ट कार्ड भेज दिया गया है, अनुमोदन के बाद आपको चैनल लिंक प्राप्त होगा।")
                else:
                    await message.reply("गिफ्ट कार्ड नंबर और पिन का फॉर्मेट सही नहीं है। कृपया 16 अंकों का कार्ड नंबर और 6 अंकों का पिन भेजें।")
            except ValueError:
                # In case the message doesn't have the expected number of parameters
                await message.reply("कृपया `/gift cardnumber cardpin` के फॉर्मेट में जानकारी भेजें।")
        else:
            await message.reply("कृपया गिफ्ट कार्ड नंबर और पिन `/gift` कमांड के साथ भेजें।")
    else:
        # If the user hasn't selected a channel yet
        await message.reply("कृपया पहले चैनल चयन करें।")
# Command handler for owner to approve gift card
@Client.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve_gift_card(bot, message: Message):
    """Approve gift card and send invite link to user."""
    try:
        logger.info(f"Owner {message.from_user.id} issued approve command.")
        if len(message.command) < 2:
            await message.reply("Usage: `/approve <user_id>`")
            return

        user_id = int(message.command[1])
        if user_id in pending_approvals:
            chat_id = pending_approvals.pop(user_id)

            # Create one-time invite link for the channel
            invite_link = await bot.create_chat_invite_link(
                chat_id=chat_id,
                member_limit=1  # Set member limit to 1
            )
            
            # Send the invite link to the user
            await bot.send_message(
                user_id,
                f"आपका गिफ्ट कार्ड सत्यापित हो गया है। यहाँ आपके लिए **वन-मेंबर लिमिट** लिंक है:\n{invite_link.invite_link}"
            )
            await message.reply(f"User {user_id} को लिंक भेज दिया गया।")
        else:
            await message.reply("यह यूजर अभी किसी भी चैनल के लिए अनुरोध लंबित नहीं है।")
    except Exception as e:
        logger.error(f"Error in approve_gift_card: {e}")
        await message.reply("लिंक भेजते समय एक त्रुटि हुई।")

# Add Channel callback handler
@Client.on_callback_query(filters.regex("add_channel"))
async def add_channel(bot, query: CallbackQuery):
    logger.info(f"User {query.from_user.id} requested to add a new channel.")
    await query.message.reply("नया चैनल जोड़ने के लिए `/add <chat_id>` कमांड का उपयोग करें।")
    await query.answer()

# Add Channel command handler (automatically fetch title)
@Client.on_message(filters.command("add"))
async def add_channel_or_group(bot, message: Message):
    """Add a new channel or group to the database by chat_id only."""
    try:
        logger.info(f"User {message.from_user.id} initiated add channel with chat_id {message.command[1]}.")
        if len(message.command) < 2:
            return await message.reply("Usage: `/add <chat_id>`", quote=True)

        chat_id = message.command[1]

        # Check if the channel/group already exists
        if collection.find_one({"chat_id": chat_id}):
            await message.reply(f"Channel with chat_id `{chat_id}` is already added.")
            return

        # Fetch the channel title using the chat_id
        try:
            chat = await bot.get_chat(chat_id)
            name = chat.title
        except Exception as e:
            await message.reply("Invalid chat_id or insufficient permissions to access this chat.")
            return

        # Insert the channel data into the database
        collection.insert_one({"name": name, "chat_id": chat_id})
        await message.reply(f"**{name}** successfully added with chat_id `{chat_id}`.")
        logger.info(f"Channel {name} added successfully with chat_id {chat_id}.")
    except Exception as e:
        logger.error(f"Error in add_channel_or_group: {e}")
        await message.reply("An error occurred while adding the channel/group.")

# Remove Channel callback handler
@Client.on_callback_query(filters.regex("remove_channel"))
async def remove_channel(bot, query: CallbackQuery):
    logger.info(f"User {query.from_user.id} requested to remove a channel.")
    await query.message.reply("चैनल हटाने के लिए `/remove <chat_id>` कमांड का उपयोग करें।")
    await query.answer()

# Command handler to remove channel by chat_id
@Client.on_message(filters.command("remove"))
async def remove_channel_or_group(bot, message: Message):
    """Remove a channel or group from the database."""
    try:
        logger.info(f"User {message.from_user.id} initiated remove channel with chat_id {message.command[1]}.")
        if len(message.command) < 2:
            return await message.reply("Usage: `/remove <chat_id>`", quote=True)

        chat_id = message.command[1]

        # Check if the channel/group exists
        channel = collection.find_one({"chat_id": chat_id})
        if not channel:
            return await message.reply(f"Channel with chat_id `{chat_id}` not found.", quote=True)

        # Remove the channel/group from the database
        collection.delete_one({"chat_id": chat_id})
        await message.reply(f"Channel with chat_id `{chat_id}` has been removed.", quote=True)
        logger.info(f"Channel with chat_id {chat_id} has been removed.")
    except Exception as e:
        logger.error(f"Error in remove_channel_or_group: {e}")
        await message.reply("An error occurred while removing the channel/group.")

# Pagination callback handler
@Client.on_callback_query(filters.regex(r"^next_page_"))
async def paginate_channels(bot, query: CallbackQuery):
    """Paginate through channel list."""
    page_num = int(query.data.split("_")[2])
    entries = list(collection.find().skip(page_num * 5).limit(5))

    buttons = [
        [InlineKeyboardButton(entry['name'], callback_data=f"link_{entry['chat_id']}")]
        for entry in entries
    ]

    # Add 'Previous Page' and 'Next Page' buttons for pagination
    if page_num > 0:
        buttons.append([InlineKeyboardButton("⬅️ Previous Page", callback_data=f"next_page_{page_num - 1}")])
    if collection.count_documents({}) > (page_num + 1) * 5:
        buttons.append([InlineKeyboardButton("➡️ Next Page", callback_data=f"next_page_{page_num + 1}")])

    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    await query.answer()
    logger.info(f"Paginated through channel list for page {page_num}.")
