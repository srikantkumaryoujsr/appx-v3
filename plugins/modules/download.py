import os
import re
import sys
import json
import time
import asyncio
import pytz
import requests
import subprocess
import plugins.modules.core as helper
from .utils import progress_bar
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pyrogram import Client, filters
from .. import bot
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

def get_current_date():
    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    yesterday = now - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    return formatted_date


def convert_timestamp_to_datetime(timestamp: int) -> str:
    date_time = datetime.utcfromtimestamp(timestamp)
    return date_time.strftime('%Y-%m-%d')


@bot.on_message(filters.command("stopji"))
async def restart_handler(_, m):
    await m.reply_text("**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


async def account_login(bot: Client, content, title, chatid):
    content = content.split("\n")
    links = []
    for i in content:
        links.append(i.split("://", 1))
    raw_text = 1
    raw_text0 = title
    raw_text2 = "360"
    if raw_text2 == "360":
        res = "640x360"
    raw_text3 = "@ImTgHacker"
    MR = raw_text3
    thumb = "no"
    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")  # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
                async with ClientSession() as session:
                    async with session.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}) as resp:
                        url = (await resp.json())['url']

            elif '/master.mpd' in url:
                id = url.split("/")[-2]
                url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'**𝐕𝐈𝐃 𝐍𝐀𝐌𝐄 :- {name1}** {res} 𝗠𝗥. 𝗛𝗔𝗖𝗞𝗘𝗥 🇮🇳.mkv\n**𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 :- {raw_text0}**\n\n**𝐂𝐋𝐀𝐒𝐒 𝐃𝐀𝐓𝐄 :- {get_current_date()}**\n\n**𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐛𝐲 :-{raw_text3}**\n\n'
                cc1 = f'**𝐏𝐝𝐟 𝐍𝐚𝐦𝐞 :- {name1}** 𝗠𝗥. 𝗛𝗔𝗖𝗞𝗘𝗥 🇮🇳.pdf \n**𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 :- {raw_text0}**\n\n**𝐏𝐃𝐅 𝐃𝐀𝐓𝐄 :- {get_current_date()}**\n\n**𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐛𝐲 :-{raw_text3}**\n\n'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        count += 1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chatid, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**📥𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠📥**\n\n**𝐍𝐚𝐦𝐞:-** `{name}\n𝐐𝐮𝐚𝐥𝐢𝐭𝐲 : - {raw_text2}`\n\n**𝐔𝐑𝐋:-** `{url}`\n𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 :- @ImTgHacker"
                    prog = await bot.send_message(chatid, text=Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, cc, filename, thumb, name, prog, chatid)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await bot.send_message(chatid, text=f"**Name** - {name}\n**Link** - {url}")
                continue

    except Exception as e:
        await bot.send_message(chat_id=chatid, text=str(e))
        await m.reply_text("❤️𝘾𝙡𝙖𝙨𝙨 𝙐𝙥𝙙𝙖𝙩𝙚 𝙆𝙖𝙧 𝘿𝙞𝙮𝙖 𝙃𝙪𝙣 , 𝙍𝙚𝙖𝙘𝙩𝙞𝙤𝙣 𝘿𝙚𝙙𝙤 𝙙𝙤𝙨𝙩𝙤𝙣❤️")
