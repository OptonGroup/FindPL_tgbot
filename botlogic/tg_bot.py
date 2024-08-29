import asyncio
import logging


from aiogram import F
from aiogram import Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.types.message import ContentType



from botlogic.settings import bot
from botlogic.handlers import base_command, database_command, admin_command
from botlogic import components




async def start_bot():
    dp = Dispatcher()
    dp.message.register(base_command.command_start_handler, Command(commands='start'))
    
    dp.message.register(base_command.get_info_handler, Command(commands='get_info'))
    dp.message.register(base_command.get_info_handler, F.text == '🤖 Профиль')
    
    dp.message.register(base_command.support_handler, Command('get_support'))
    dp.message.register(base_command.support_handler, F.text == '💬 Помощь')
    
    dp.message.register(database_command.buy_sub_handler, Command('buy_sub'))
    dp.message.register(database_command.buy_sub_handler, F.text == '⭐️ Купить Подписку')
    dp.message.register(database_command.successful_payment_handler, F.successful_payment)
    dp.pre_checkout_query.register(database_command.pre_checkout_query, lambda query: True)
    
    dp.message.register(database_command.get_town_keyboard_handler, Command('change_town'))
    dp.message.register(database_command.get_town_keyboard_handler, F.text == '🏙 Сменить Город')
    dp.message.register(database_command.change_town_handler, F.text.lower().in_({'москва', 'санкт-петербург', 'екатеринбург', 'краснодар'}))    
    
    dp.message.register(admin_command.admin_commands_handler, Command('admin_commands'))
    dp.message.register(admin_command.secret_code_handler, Command('get_admin_25634'))
    dp.message.register(admin_command.get_user_by_id_handler, Command('get_user_by_id'))
    dp.message.register(admin_command.get_user_by_username_handler, Command('get_user_by_name'))
    dp.message.register(admin_command.give_admin_handler, Command('give_admin'))
    dp.message.register(admin_command.remove_admin_handler, Command('remove_admin'))
    dp.message.register(admin_command.get_users_handler, Command('get_users_info'))
    dp.message.register(admin_command.get_logs_handler, Command('get_logs'))
    dp.message.register(admin_command.give_sub_handler, Command('give_sub'))
    
    dp.callback_query.register(database_command.process_callback_button_ref, lambda query: query)
    dp.message.register(database_command.capture_referral_username, StateFilter(components.Form.referral_username))
        
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s"
    )
    
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_bot())
    loop.run_until_complete(task)