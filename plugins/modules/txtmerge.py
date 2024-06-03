from pyrogram import filters, idle
from .. import bot as app
import requests, asyncio, os

LOG_CHANNEL_ID = -1001801766701
AUTH_USERS = [6748451207, 6804421130, 6671207610]

@app.on_message(filters.private & filters.command("merge"))
async def merge_files(client, message):
    user_id = message.from_user.id
    if user_id not in AUTH_USERS:
        await message.reply("**𝐁𝐚𝐛𝐲 𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐌𝐞𝐦𝐛𝐞𝐫 😂 आया बड़ा फ्री यूज करने **")
        return

    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("Reply to a document")

    documents = []
    for i in range(message.reply_to_message.id, message.id + 1):
        current_message = await client.get_messages(message.chat.id, i)
        if current_message.document:
            documents.append(current_message.document.file_id)

    print(documents)
    files_to_merge = []
    for document in documents:
        file_path = f"downloads/{document}.txt"
        await client.download_media(document, file_name=file_path)
        files_to_merge.append(file_path)

    merged_text = ""
    for file_path in files_to_merge:
        with open(file_path, "r") as file:
            merged_text += file.read() + "\n"
        os.remove(file_path)

    with open("merged.txt", "w") as merged_file:
        merged_file.write(merged_text)

    await client.send_document(message.chat.id, "merged.txt", caption="Files merged successfully! 🚀")
    await client.send_document(LOG_CHANNEL_ID, "merged.txt", caption="Files merged successfully! 🚀")
    os.remove("merged.txt")
