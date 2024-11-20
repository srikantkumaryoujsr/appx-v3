import pyrogram
from .. import bot as Client
from pymongo import MongoClient
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram import Client, filters
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
import time
import asyncio
from pyrogram.types import User, Message
from config import *
import sys
import re
import os
import aiohttp
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .. import bot as Client

MONGO_URI = "mongodb+srv://stoner:ZrGD9K3ZPjsw6rVd@cluster0.tl9sc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 

client = MongoClient(MONGO_URI)
db = client["bot_database"]  
subscriptions = db["subscriptions"]  

ADMINS = [7015210460,7224758848] 

def add_subscription(user_id, days=30):
    """Add or extend a subscription for a user."""
    expires_at = datetime.utcnow() + timedelta(days=days)
    subscriptions.update_one(
        {"user_id": user_id},
        {"$set": {"expires_at": expires_at}},
        upsert=True
    )

def check_subscription(user_id):
    """Check if a user's subscription is active."""
    user = subscriptions.find_one({"user_id": user_id})
    if user and "expires_at" in user:
        return user["expires_at"] > datetime.utcnow()
    return False

def get_subscription_status(user_id):
    """Get a user's subscription expiration date."""
    user = subscriptions.find_one({"user_id": user_id})
    if user and "expires_at" in user:
        return user["expires_at"]
    return None

def remove_subscription(user_id):
    """Remove a user's subscription."""
    result = subscriptions.delete_one({"user_id": user_id})
    return result.deleted_count > 0


@Client.on_message(filters.command("subscribe") & filters.user(ADMINS))
async def subscribe_user(bot, m: Message):
    """Admin command to add a subscription for a user."""
    try:
        _, user_id, days = m.text.split()
        user_id = int(user_id)
        days = int(days)
        add_subscription(user_id, days)
        await m.reply_text(f"✅ User {user_id} subscribed for {days} days.")
    except Exception as e:
        await m.reply_text(f"❌ Failed to add subscription: {e}")

@Client.on_message(filters.command("myplan"))
async def my_plan(bot, m: Message):
    """Check the subscription details for the current user."""
    try:
        user_id = m.from_user.id
        expires_at = get_subscription_status(user_id)
        if expires_at:
            status = "Active" if expires_at > datetime.utcnow() else "Expired"
            await m.reply_text(
                f"📋 **Your Subscription Details**:\n"
                f"**Status**: {status}✅\n"
                f"**Expires At**: {expires_at}"
            )
        else:
            await m.reply_text("❌ You do not have an active subscription.")
    except Exception as e:
        await m.reply_text(f"❌ Error checking your plan: {e}")

@Client.on_message(filters.command("status") & filters.user(ADMINS))
async def subscription_status(bot, m: Message):
    """Check the subscription status of a user."""
    try:
        user_id = int(m.text.split()[1])
        expires_at = get_subscription_status(user_id)
        if expires_at:
            status = "🟢Active🟢" if expires_at > datetime.utcnow() else "Expired"
            await m.reply_text(f"User {user_id}:\n**Status**: {status}\n**Expires At**: {expires_at}")
        else:
            await m.reply_text(f"User {user_id} is not subscribed.")
    except Exception as e:
        await m.reply_text(f"❌ Error checking status: {e}")

@Client.on_message(filters.command("remove") & filters.user(ADMINS))
async def remove_user_subscription(bot, m: Message):
    """Admin command to remove a subscription for a user."""
    try:
        user_id = int(m.text.split()[1])
        if remove_subscription(user_id):
            await m.reply_text(f"✅ User {user_id}'s subscription has been removed.")
        else:
            await m.reply_text(f"❌ User {user_id} does not have a subscription.")
    except Exception as e:
        await m.reply_text(f"❌ Error removing subscription: {e}")
