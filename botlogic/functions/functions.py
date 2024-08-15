import asyncio
from dblogic.database import database
from botlogic.settings import bot

async def send_ads(ads, town):
    for user in database.get_users(town=town, sub_active=True):
        for ad in ads:
            await bot.send_message(chat_id=user[1], text=ad)
            await asyncio.sleep(0.15)