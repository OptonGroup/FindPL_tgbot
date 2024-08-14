import asyncio
import logging


from aiogram import F
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types.message import ContentType



from botlogic.settings import bot
from botlogic.handlers import base_command, database_command




async def start_bot():
    dp = Dispatcher()
    dp.message.register(base_command.command_start_handler, Command(commands='start'))
    
    dp.message.register(base_command.get_info_handler, Command(commands='get_info'))
    dp.message.register(base_command.get_info_handler, F.text == '👤 Профиль')
    
    dp.message.register(base_command.support_handler, Command('get_support'))
    dp.message.register(base_command.support_handler, F.text == '💬 Тех. Поддержка')
    
    dp.message.register(database_command.buy_sub_handler, Command('buy_sub'))
    dp.message.register(database_command.buy_sub_handler, F.text == '🛒 Купить Подписку')
    dp.message.register(database_command.successful_payment_handler, F.successful_payment)
    dp.pre_checkout_query.register(database_command.pre_checkout_query, lambda query: True)
    
    dp.message.register(database_command.get_town_keyboard_handler, Command('change_town'))
    dp.message.register(database_command.get_town_keyboard_handler, F.text == '🌆 Сменить Город')
    
    dp.message.register(database_command.change_town_handler, F.text.lower().in_({'москва', 'санкт-петербург', 'екатеринбург', 'краснодар'}))    
    
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s"
    )
    
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_bot())
    loop.run_until_complete(task)