import asyncio
from dblogic.database import database
from botlogic.settings import bot

async def send_text(text):
    for user in database.get_users():
        try:
            await bot.send_message(chat_id=user[1], text=text)
        except:
            pass

async def send_ads(ads, town):
    for user in database.get_users(town=town, sub_active=1):
        for ad in ads:
            try:
                if user[11] <= ad[1] <= user[12]:
                    await bot.send_message(chat_id=user[1], text=ad[0])
            except:
                pass
            await asyncio.sleep(0.07)
    
    
    for user in database.get_users(town=town, sub_active=-1):
        for ad in ads:
            try:
                await bot.send_message(chat_id=user[1], text=ad[0])
            except:
                pass
            await asyncio.sleep(0.07)
