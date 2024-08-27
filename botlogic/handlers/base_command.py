from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from botlogic.handlers.database_command import identification_user
from botlogic.components import keyboard

town_translate = {'москва': 'moskva', 'moskva': 'москва', 'санкт-петербург': 'sankt-peterburg', 'sankt-peterburg': 'санкт-петербург', 'екатеринбург': 'ekaterinburg', 'ekaterinburg': 'екатеринбург', 'краснодар': 'krasnodar', 'krasnodar': 'краснодар'}



async def command_start_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)

    user_info = await state.get_data()
    await message.answer(
        f'''<b>Что может делать этот бот?</b>\nБот Kv/M уведомляет обо всех новых объявлениях на площадке Авито о снятии квартир в городах  Москва, Санкт-Петербург, Екатеринбург, Краснодар.\nВам доступна подписка до <code>{user_info['sub_end']}</code>''',
        reply_markup=keyboard
    )
    

async def get_info_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    user_info_text = f'''
ℹ️ Профиль
- - - - - - - - - - - - - - - - - - - - - - - -

🕑 Подписка до <code>{user_info['sub_end']}</code>
🌆Город поиска: <code>{town_translate[user_info['town_search']].capitalize()}</code>
🔑 ID: <code>{user_info['tg_id']}</code>
▫️ Username: <code>{user_info['username']}</code>

- - - - - - - - - - - - - - - - - - - - - - - -
    '''
    await message.answer(user_info_text, reply_markup=keyboard)
    

async def support_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        '''
Оплата подписки через Telegram Stars ⭐️

Вы можете приобрести звезды через @PremiumBot

О нашем сервисе:

С помощью нашего бота вы сможете оперативно дозваниваться до собственников, благодаря чему вы сможете быть первым в очереди на просмотр.

Некоторые риэлторы тоже дозваниваются первыми через аналогичный сервис, далее выставляют квартиры уже с комиссией. Наш бот поможет вам быть быстрее.

Поддержка: @s1cptn
        ''',
        reply_markup=keyboard
    )
