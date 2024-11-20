import asyncio
import os
import aiohttp
import aiofiles
import base64,requests
from pyrogram.types import Message
from pyrogram import Client, filters
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from .. import bot as Client
from plugins.modules.subscription import check_subscription

LOG_CHANNEL_ID = -1001801766701



async def fetch_data(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

def decrypt_link(link):
    try:
        decoded_link = base64.b64decode(link.encode('utf-8'))
        key = b'638udh3829162018'
        iv = b'fedcba9876543210'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_link = unpad(cipher.decrypt(decoded_link), AES.block_size).decode('utf-8')
        return decrypted_link
    except ValueError:
        pass
    except Exception:
        pass

cc02 = ""
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjUxNzA3NyIsImVtYWlsIjoidml2ZWtrYXNhbmE0QGdtYWlsLmNvbSIsInRpbWVzdGFtcCI6MTcyNjkzNzA4OX0.NM1SbOjDFZCLinFi66jKxwRQPgLWFN-_SAMgcPWvfk4"

@Client.on_message(filters.command("rwa"))
async def account_login(bot: Client, m: Message):
    if not check_subscription(m.from_user.id):
        await m.reply_text("**❌ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.🟠🟢🔴**\n\n**🟡☢️ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ꜱᴜʙꜱᴄʀɪʙᴇ.🔵❤️**")
        return
    editable = await m.reply_text("🟢🟡🔵𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐛𝐚𝐭𝐜𝐡 𝐝𝐞𝐭𝐚𝐢𝐥𝐬... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭.🟢🟡🔵")

    headers = {
        'auth-key': 'appxapi',
        'authorization': TOKEN,
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }

    try:
        async with aiohttp.ClientSession() as session:
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={m.from_user.id}", headers=headers)
            bdetail = res1.get("data", [])
            if not bdetail:
                await editable.edit("No courses found for this account.")
                return

            cool = ""
            FFF = "**BATCH-ID -      BATCH NAME **"
            for item in bdetail:
                id = item.get("id")
                batch = item.get("course_name")
                aa = f" {id}      - *{batch}*\n\n"
                if len(f'{cool}{aa}') > 4096:
                    with open("batch_details.txt", "w", encoding="utf-8") as f:
                        f.write(f'{FFF}\n\n{cool}')
                    await m.reply_document(document="batch_details.txt", caption="Batch details (file format due to large message size)")
                    os.remove("batch_details.txt")
                    cool = aa
                else:
                    cool += aa

            if len(cool) <= 4096:
                await editable.edit(f'{"*🔵🟡🟢𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐭𝐡𝐞𝐬𝐞 𝐛𝐚𝐭𝐜𝐡𝐞𝐬 :-🔵🟡🟢*"}\n\n{FFF}\n\n{cool}')

            editable1 = await m.reply_text("*Now send the Batch ID to Download*")
            user_id = m.from_user.id

            if user_id is not None and user_id not in AUTH_USERS:
                await m.reply("*PLEASE UPGRADE YOUR PLAN*", quote=True)
                return
            else:
                input2 = await bot.listen(editable.chat.id)
                raw_text2 = input2.text
                bname = next((x['course_name'] for x in bdetail if str(x['id']) == raw_text2), None)
                await input2.delete()
                await editable.delete()
                await editable1.delete()
                edit3 = await m.reply_text(f"""Now send the quality you want to download:
`720p`
`360p`
`240p`
`144p`""")
                input3 = await bot.listen(edit3.chat.id)
                if input3.text not in ["720p", "360p", "240p", "144p"]:
                    return await edit3.edit_text("Enter valid quality, try again.")

                editable2 = await m.reply_text("🔵🟡🟢𝐘𝐨𝐮𝐫 𝐁𝐚𝐭𝐜𝐡 𝐓𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐰𝐚𝐢𝐭 [ 𝟐 𝐦𝐢𝐧𝐮𝐭𝐬 𝐬𝐞 𝟐 𝐠𝐡𝐚𝐧𝐭𝐞 𝐭𝐚𝐤🔵🟡🟢")

                res2 = requests.get(f"https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid={raw_text2}&start=-1", headers=headers).json()
                subject = res2.get("data", [])
                subjID = "&".join([id["subjectid"] for id in subject])
                subject_ids = subjID.split('&')
                all_urls = ""
                topicids = []

                for u in subject_ids:
                    res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={u}&start=-1", headers=headers)
                    topic = res3.get("data", [])
                    topicids.extend([i["topicid"] for i in topic])

                courseid = []
                for t in topicids:
                    url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid={raw_text2}&subjectid={u}&topicid={t}&start=-1&conceptid="
                    res4 = requests.get(url, headers=headers).json()
                    videodata = res4.get("data", [])
                    for i in videodata:
                        courseid.append(i["id"])

                for c in courseid:
                    url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id={raw_text2}&video_id={c}&ytflag=0&folder_wise_course=0"
                    await asyncio.sleep(2)
                    res4 = await fetch_data(session, url, headers=headers)
                    data = res4.get("data", [])
                    title = data.get("Title")
                    video = data.get('download_link', None)
                    if video is not None:
                        video2 = decrypt_link(video.replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0])
                        if video2 is not None:
                            all_urls += f"{title} : {video2}\n"

                    pdf_1 = data.get('pdf_link')
                    if pdf_1:
                        pdf_1 = decrypt_link(pdf_1.replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0])
                        all_urls += f"{title} : {pdf_1}\n"

                    pdf_2 = data.get('pdf_link2')
                    if pdf_2:
                        pdf_2 = decrypt_link(pdf_2.replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0])
                        all_urls += f"{title} : {pdf_2}\n"

                all_urls = all_urls.replace("720p", input3.text)
                if all_urls:
                    with open(f"results.txt", 'w', encoding='utf-8') as f:
                        f.write(all_urls)

                    await m.reply_document(
                        document=f"results.txt",
                        caption=f"App Name: Rojgar With Ankit\nBatch Name: {bname}\nExtracted by  :- User"
                    )
                    await bot.send_document(LOG_CHANNEL_ID,
                        document=f"results.txt",
                        caption=f"App Name: Rojgar With Ankit\nBatch Name: {bname}\nExtracted by  :- User"
                    )

    except Exception as e:
        print(f"An error occurred: {e}")
        await m.reply(f"An error occurred. Please try again. Error: {e}")
