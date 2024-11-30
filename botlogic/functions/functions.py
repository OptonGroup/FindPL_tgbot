import asyncio
from dblogic.database import database
from botlogic.settings import bot
import logging
from botlogic import components


async def send_alarm_active():
    for user in database.get_users_no_active():
        try:
            logging.info(f'No active from user tg_id={user[1]}')
            await bot.send_message(
                chat_id=user[1],
                text=f'''Вы не проявляли активность в течении 2х и более дней. Когда вы снова захотите получать уведомления - нажмите на кнопку ниже и они начнут приходить (это сделано в целях экономии пропускной способности)''',
                reply_markup=components.start_work_button
            )
        except:
            pass

async def send_ads(ads, town):
    for user in database.get_users(town=town, sub_active=1, last_active=True):
        user_status = await bot.get_chat_member(chat_id=-1002080804090, user_id=user[1])
        if user_status.status == 'left':
            continue
        for ad in ads:
            try:
                if user[11] <= ad[1] <= user[12]:
                    await bot.send_message(chat_id=user[1], text=ad[0])
            except:
                pass
            await asyncio.sleep(0.07)
