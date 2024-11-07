import asyncio
import aiohttp, requests
import base64, time
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram import Client as bot
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import datetime
LOG_CHANNEL_ID = -1001801766701

def convert_timestamp_to_datetime(timestamp: int) -> str:
    date_time = datetime.datetime.utcfromtimestamp(timestamp)
    formatted_date_time = date_time.strftime('%Y-%m-%d')
    return formatted_date_time

async def fetch_data(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json()

def decrypt_link(link):
    try:
        decoded_link = base64.b64decode(link)
        key = b'638udh3829162018'
        iv = b'fedcba9876543210'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_link = unpad(cipher.decrypt(decoded_link), AES.block_size).decode('utf-8')
        return decrypted_link
    except ValueError as ve:
        print(f"Padding error while decrypting link: {ve}")
    except Exception as e:
        print(f"Error decrypting link: {e}")

@bot.on_message(filters.command(["fghfghfg"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    input1 = await bot.listen(editable.chat.id)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'auth-key': 'appxapi',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    raw_text = input1.text
    await input1.delete(True)
    async with aiohttp.ClientSession() as session:
        try:
            if "*" in raw_text:
                email, password = raw_text.split("*")
                payload = {"email": email, "password": password}
                url = f"https://rozgarapinew.teachx.in/post/userLogin?extra_details=0"
                async with session.post(url, data=payload, headers=headers) as response:
                    login = await response.json()
                    login_data = login.get("data", {})
                    userid = login_data.get("userid", '')
                    token = login_data.get("token", '')
            else:
                token = raw_text
                hdr1 = {
                    'auth-key': 'appxapi',
                    'authorization': token,
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9'
                }
                userid = ""
                await editable.edit("**🎁 login Successful 🎁**")
 
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=hdr1)
            bdetail = res1.get("data", [])
            cool = ""
            FFF = "**BATCH-ID -      BATCH NAME **"
            for item in bdetail:
                id = item.get("id")
                batch = item.get("course_name")
                aa = f" `{id}`      - **{batch}**\n\n"
                if len(f'{cool}{aa}') > 4096:
                    print(aa)
                    cool = ""
                cool += aa
            await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
            editable1 = await m.reply_text("**Now send the Batch ID to Download**")

            input2 = await bot.listen(editable.chat.id)
            raw_text2 = input2.text
            bname = next((x['course_name'] for x in bdetail if str(x['id']) == raw_text2), None)
            await input2.delete(True)
            await editable.delete()
            await editable1.delete()
            edit3 = await m.reply_text(f"""Now send the  quality u want to download
`720p`
`360p`
`240p`
`144p`""")
            input3 = await bot.listen(edit3.chat.id)
            if input3.text not in ["720p", "360p", "240p", "144p"]:
                return await edit3.edit_text("enter valid quality try again")

            await edit3.delete()
            res2 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid={raw_text2}&start=-1", headers=hdr1)
            subject = res2.get("data", [])
            
            subject_name = [(sn["subject_name"]) for sn in subject]
            subjID = "&".join([i["subjectid"] for i in subject])
            print(f'All Subject Id Info: \n{subjID}')
            subject_ids = subjID.split('&')
            subject_info = {key: value for key, value in zip(subject_ids, subject_name)}
            await m.reply(f"""All Subjects id: name\n{chr(10).join([f'{x}: {y}' for x, y in subject_info.items()])}""")
            edit6 = await m.reply_text(f"""Now send the subject IDs you want to download 📚""")
            input6 = await bot.listen(edit6.chat.id)
            subjects_ids_input = input6.text.split("&") if "&" in input6.text else [input6.text]
            for sub in subjects_ids_input:
                if sub not in subject_ids:
                    return await edit6.edit_text("Enter a valid subject ID, please try again 🔄")

            all_important = {}
            for u in subjects_ids_input:
                res3 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={u}&start=-1", headers=hdr1)
                topic = res3.get("data", [])
                
                topicids = [i["topicid"] for i in topic]
                all_urls = ""
        
                couserid = []
                videos = []
                all_important = {}
                for t in topicids:
                    url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid={raw_text2}&subjectid={u}&topicid={t}&start=-1&conceptid="
                    
                    res4 = await fetch_data(session, url, headers=hdr1)
                    videodata = res4.get("data", [])
                    try:
                        for i in videodata:
                            couserid.append(i["id"])
                            
                    except Exception as e:
                        print(e)
                for c in couserid:
                    url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id={raw_text2}&video_id={c}&ytflag=0&folder_wise_course=0"
                    res4 = requests.get(url, headers=hdr1).json()
                    video = res4.get("data", [])
                    videos.append(video)
                    
                
                for i in videos:
                    try:
                        all_important[convert_timestamp_to_datetime(i["strtotime"])] = {
                        "title": i["Title"],
                        'pdf_link': decrypt_link(i['pdf_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link") else "",
                        'pdf_link2': decrypt_link(i['pdf_link2'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]) if i.get("pdf_link2") else "",
                        'download_link': decrypt_link(i['download_link'].replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0]).replace("720p", "360p")}
                    except Exception:
                        pass

            edit4 = await m.reply_text(f"""Now send me the date for which you want the lecture 📅
    # Format: yyyy-mm-dd
    {chr(10).join([key for key in all_important.keys()])}""")
            input4 = await bot.listen(edit4.chat.id)
            if input4.text not in all_important.keys():
                return await edit4.edit_text("Enter a valid date, please try again 🔄")
                    
            data = all_important[input4.text]
            title = data.get("title")
            all_urls = ""
            video = data.get("download_link","")
            pdf_1 = data.get("pdf_link","")
            pdf_2 = data.get("pdf_link2","")
            all_urls += f"{title} : {video}\n{title} : {pdf_1}\n{title} : {pdf_2}"
            print(all_urls)

            if all_urls:
                with open(f"{title[:10]}.txt", 'w', encoding='utf-8') as f:
                    f.write(all_urls)

            await m.reply_document(
                document=f"{title[:10]}.txt",
                caption=f"📕 TEXT FILE 📕\n❤️ APPLICATION NAME ❤️: Rojgar With Ankita 🌟\n🔰 BATCH NAME 🔰: {bname}\nTopic Name : {title[:10]}"
            )
            await bot.send_document(LOG_CHANNEL_ID,
                document=f"{title[:10]}.txt",
                caption=f"📕 TEXT FILE 📕\n❤️ APPLICATION NAME ❤️: Rojgar With Ankita 🌟\n🔰 BATCH NAME 🔰: {bname}\nTopic Name : {title[:10]}"
            )

        except Exception as e:
            print(f"An error occurred: {e}")
            await m.reply("An error occurred. Please try again.")
