from RenaBot.config import client as C
from telethon import events,Button
from FastTelethonhelper import download_without_progressbar
from FastTelethonhelper import upload_without_progress_bar
from telethon.utils import is_image
import os


@C.on(events.NewMessage(pattern="/setthumb"))
async def thumb(event):
    reply=await event.get_reply_message()
    if is_image(reply):
        thumb = await C.download_media(reply.photo)
        with open(thumb, "rb") as i:
            Pic = i.read()
        with open(f"Thumbs\\{event.peer_id.user_id}.png", "wb") as i:
            i.write(Pic)
        await event.reply("Image set as thumb.")
        os.remove(thumb)
    else:
        await event.reply("Image not found.")
    
@C.on(events.NewMessage(pattern="/rename"))
async def renamer(event):
    text=event.raw_text
    text=text.split(" ",maxsplit=1)[1]
    reply=await event.get_reply_message()
    if event.is_reply:
        pass
    else:
        return
    await event.reply("Please wait while we rename your file.")
    download=await download_without_progressbar(client=C,msg=reply)
    download_ext='.'+download.split(".")[-1]
    await event.reply("Please wait while we upload your file.")
    if os.path.exists(f"{event.peer_id.user_id}.png"):
        await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=text+download_ext,thumbnail=f"Thumbs\\{event.peer_id.user_id}.png")
    else:
        await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=text+download_ext)
@C.on(events.NewMessage(pattern="/batchrename"))
async def batchrenamer(event):
    real_text=""
    text=event.raw_text
    text=text.split(" ")
    number=text.pop()
    for i in range(0,len(text)):
        text[i]=text[i].replace("batchrename",'')
    for i in text:
        real_text=real_text+i+" "
    if ".zzz"in number:
        number=number.replace(".zzz","")
        number.strip()
        j=int(number)
    else:
        j=1
    reply=await event.get_reply_message()
    current_id=event.id
    reply_id=reply.id
    await event.reply('Starting Process, sit back & relax, this might take a while.')
    for i in range(reply_id,current_id):
        try:
            x = await C.get_messages(event.chat_id, ids=i)
            download=await download_without_progressbar(client=C,msg=x)
            download_ext='.'+download.split(".")[-1]
            if os.path.exists(f"{event.peer_id.user_id}.png"):
                await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=real_text+str(j)+download_ext,thumbnail=f"Thumbs\\{event.peer_id.user_id}.png")
            else:
                await upload_without_progress_bar(client=C,entity=event.chat_id,file_location=download, name=real_text+str(j)+download_ext)
            os.remove(download)
            j=j+1
        except:
            j=j+1
            pass
    await event.reply(f"Process finished.")
        
@C.on(events.NewMessage(pattern="/autoforward"))
async def rem(event):
    text=event.raw_text
    text=text.split(" ",maxsplit=1)[1]
    reply=await event.get_reply_message()
    current_id=event.id
    reply_id=reply.id
    text=text.strip()
    text2='-100'+text
    try:
        text1=int(text2)
        for i in range(reply_id,current_id):
            x = await C.get_messages(event.chat_id, ids=i)
            await C.send_message(int(text1),x)
    except:
        for i in range(reply_id,current_id):
            x = await C.get_messages(event.chat_id, ids=i)
            await C.send_message(text,x)
        
@C.on(events.NewMessage(pattern="/remthumb"))
async def rem(event):
    text=event.raw_text
    text=text.split(" ",maxsplit=1)[1]
    
    if os.path.exists(f"Thumbs\\{event.peer_id.user_id}.png"):
        os.remove(f"Thumbs\\{event.peer_id.user_id}.png")
        await event.reply("Thumb Deleted.")
        return               
    else:
        await event.reply("You haven't set a thumb.")
