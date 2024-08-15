from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from botlogic.handlers.database_command import identification_user


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="🛒 Купить Подписку"),
        ],
        [
            KeyboardButton(text="🌆 Сменить Город"),
            KeyboardButton(text="💬 Тех. Поддержка"),
        ]
    ],
    resize_keyboard=True
)

town_translate = {'москва': 'moskva', 'moskva': 'москва', 'санкт-петербург': 'sankt-peterburg', 'sankt-peterburg': 'санкт-петербург', 'екатеринбург': 'ekaterinburg', 'ekaterinburg': 'екатеринбург', 'краснодар': 'krasnodar', 'krasnodar': 'краснодар'}



async def command_start_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)

    await message.answer(
        '<b>Что может делать этот бот?</b>\nБот FindPL уведомляет обо всех новых объявлениях на площадке Авито о снятии квартир в городах  Москва, Санкт-Петербург, Екатеринбург, Краснодар',
        reply_markup=keyboard
    )
    

async def get_info_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    user_info_text = f'''ℹ️ Профиль\n- - - - - - - - - - - - - - - - - - - - - - - -\n\n🕑 Подписка до <code>{user_info['sub_end']}</code>\n🌆Город поиска: <code>{town_translate[user_info['town_search']].capitalize()}</code>\n🔑 ID: <code>{user_info['tg_id']}</code>\n▫️ Username: <code>{user_info['username']}</code>\n\n- - - - - - - - - - - - - - - - - - - - - - - -'''
    await message.answer(user_info_text, reply_markup=keyboard)
    

async def support_handler(message: Message, state: FSMContext) -> None:
    await message.answer('@s1cptn', reply_markup=keyboard)