import asyncio
import aiohttp
import aiofiles
import base64,requests
from pyrogram.types import Message
from pyrogram import Client, filters
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from .. import bot as Client
LOG_CHANNEL_ID = -1001801766701
AUTH_USERS = [6748451207, 6804421130,6728038801,5565127109,6776883780,6741261680,6773081023,6793357832,7224758848]
 
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
cc02=""
@Client.on_message(filters.command("rwa"))
async def account_login(bot: Client, m: Message):
    global token
    editable = await m.reply_text("Send *ID & Password* in this manner otherwise bot will not respond.\n\nSend likeh this:-  *ID*Password*")
    input1 = await bot.listen(editable.chat.id)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'auth-key': 'appxapi',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    raw_text = input1.text
    user_id = input1.from_user.id
    print("Opponent's user_id:", user_id)
    await input1.delete(True)
    
    headers2={
            'Content-Type': 'application/x-www-form-urlencoded',
            'auth-key': 'appxapi',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            "Origin": "https://rojgarwithankit.co.in",
            "Referer": "https://rojgarwithankit.co.in/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    async with aiohttp.ClientSession() as session:
        try:
            if '*' in raw_text:
                email, password = raw_text.split('*')
                if email and password:
                    payload = {"source": "website", "email": email, "password": password, "extra_details": 1}
                    url = "https://rozgarapinew.teachx.in/post/userLogin"
                    async with session.post(url, data=payload, headers=headers2) as response:
                        login = await response.json()
                        login_data = login.get("data", {})
                        token = login_data.get("token", '')
                        if token:
                            await m.reply_text(f"🤡𝐘𝐨𝐮𝐫 𝐓𝐨𝐤𝐞𝐧 𝐟𝐨𝐫 𝐑𝐨𝐣𝐠𝐚𝐫𝐰𝐢𝐭𝐡𝐚𝐧𝐤𝐢𝐭🤡:\n\n `{token}`")
                        else:
                            await m.reply_text("Failed to retrieve token.")
            else:
                token = raw_text

            headers = {
                'auth-key': 'appxapi',
                'authorization': token,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9'
            }
            userid = ""
            await editable.edit("**🤡 𝐥𝐨𝐠𝐢𝐧 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥 🤡**")
            headers = {
            'auth-key': 'appxapi',
            'authorization': token,
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9'
                }
            print(headers['authorization'])
            res1 = await fetch_data(session, f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=headers)

            print("88",res1)
            res1=requests.get(f"https://rozgarapinew.teachx.in/get/mycourse?userid={userid}", headers=headers).json()
            # print(h)
            print("91",res1)
            bdetail = res1.get("data", [])
            courseid=[]
            cool = ""
            FFF = "**BATCH-ID -      BATCH NAME **"
            for item in bdetail:
                id = item.get("id")
                batch = item.get("course_name")
                aa = f" {id}      - *{batch}*\n\n"
                # Check if adding the current batch will exceed the character limit
                if len(f'{cool}{aa}') > 4096:
                    # If it exceeds, send the current batch info and reset `cool`
                    await editable.edit(f'{"*You have these batches :-*"}\n\n`{FFF}`\n\n{cool}')
                    cool = ""  # Reset cool to start the next batch message
                cool += aa

            # If there are remaining batches to be sent, send them
            if cool:
                await editable.edit(f'{"*You have these batches :-*"}\n\n`{FFF}`\n\n{cool}')

            editable1 = await m.reply_text("*Now send the Batch ID to Download*")
            print("User ID:", m.from_user.id)
            print("AUTH_USERS:", AUTH_USERS)
 
            if user_id is not None and user_id not in AUTH_USERS:
                print("User ID not in AUTH_USERS")
                await m.reply("*PLEASE UPGRADE YOUR PLAN*", quote=True)
                return
            else:
                input2 = await bot.listen(editable.chat.id)
                raw_text2 = input2.text
                bname = next((x['course_name'] for x in bdetail if str(x['id']) == raw_text2), None)
                await input2.delete(True)
                await editable.delete()
                await editable1.delete()
                edit3=await m.reply_text(f"""Now send the  quality u want to download
720p
360p
240p
144p""")
                input3 = await bot.listen(edit3.chat.id)
                if input3.text not in ["720p","360p","240p","144p"]:
                    return await edit3.edit_text("enter valid quality try again")
                
                editable2 = await m.reply_text("Thoda Intzar Kariye , itni bhi kya jaldi hai , Aayegi TXT tabtak Chay pijiye")
                res2 = requests.get(f"https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid={raw_text2}&start=-1", headers=headers).json()
                subject = res2.get("data", [])
                subjID = "&".join([id["subjectid"] for id in subject])
                print(f'All Subject Id Info: {subjID}')
                subject_ids = subjID.split('&')
                all_urls = ""
                topicids=[]
                title=""
                for u in subject_ids:
                    res3 = await fetch_data(session,f"https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid={raw_text2}&subjectid={u}&start=-1", headers=headers)
                    topic = res3.get("data", [])
                    topicids.extend([i["topicid"] for i in topic])
       
                    for t in topicids:
                        url = f"https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?courseid={raw_text2}&subjectid={u}&topicid={t}&start=-1&conceptid="
    
                        res4 = requests.get(url, headers=headers).json()
                        videodata = res4.get("data", [])
                       
                        for i in videodata:
                            courseid.append(i["id"])
                            # print(i)
                    
                print(courseid)
                try:
                    for c in courseid:
                        print(c)
                        url = f"https://rozgarapinew.teachx.in/get/fetchVideoDetailsById?course_id={raw_text2}&video_id={c}&ytflag=0&folder_wise_course=0"
                        # print(url)
                        await asyncio.sleep(2)
                        res4 = await fetch_data(session, url, headers=headers)
                        data = res4.get("data", [])
                        # print(data["Title"])
                        title=data.get("Title")
                        video = data.get('download_link',None)
                        # print(video)
                        if video is not None:
                            video2 = decrypt_link(video.replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0])
                            print(video2)
                            if video2 is not None:
                                all_urls += f"{title} : {video2}\n"
                        pdf_1 = data.get('pdf_link')
                        if pdf_1:
                            pdf_1 = decrypt_link(pdf_1.replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0])
                            all_urls+=f"{title} : {pdf_1}\n"

                        pdf_2 = data.get('pdf_link2')
                        if pdf_2:
                            pdf_2 = decrypt_link(pdf_2.replace(":", "=").replace("ZmVkY2JhOTg3NjU0MzIxMA", "==").split(',')[0])
                            all_urls+=f"{title} : {pdf_2}\n"
                        
                        all_urls=all_urls.replace("720p",input3.text)
                        if all_urls:
                            with open(f"results.txt", 'w', encoding='utf-8') as f:
                                f.write(all_urls)
                    
                    await m.reply_document(
                                document=f"results.txt",
                                caption=f"App Name: Rojgar With Ankit\nBatch Name: {bname}\nExtracted by  :- Chutiya"
                        )
                    await bot.send_document(LOG_CHANNEL_ID,
                                document=f"results.txt",
                                caption=f"App Name: Rojgar With Ankit\nBatch Name: {bname}\nExtracted by  :- Chutiya"
                        )
                except Exception as e:
                    pass
                    print(e)
                    await m.reply_document(
                                document=f"results.txt",
                                caption=f"App Name: Rojgar With Ankit\nBatch Name: {bname}\nExtracted by  :- Chutiya"
                        )
                    await bot.send_document(LOG_CHANNEL_ID,
                                document=f"results.txt",
                                caption=f"App Name: Rojgar With Ankit\nBatch Name: {bname}\nExtracted by  :- Chutiya"
                        )
                    await m.reply_text(f"""Done âœ…

Your Token for : Rojgarwithankit  {token}""")
                 
        except Exception as e:
            print(f"An error occurred: {e}")
            
            await m.reply(f"An error occurred. Please try again.{e}")
