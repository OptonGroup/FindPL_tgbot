from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.fsm.state import State, StatesGroup

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🤖 Профиль"),
            KeyboardButton(text="⭐️ Купить Подписку"),
        ],
        [
            KeyboardButton(text="🏙 Сменить Город"),
            KeyboardButton(text="💬 Помощь"),
        ],
        [
            KeyboardButton(text="⚙️ Фильтр Цены"),
        ]
    ],
    resize_keyboard=True
)


inline_start_list = [
    [InlineKeyboardButton(text="Ввести username друга", callback_data='add_referral')],
]
start_button = InlineKeyboardMarkup(inline_keyboard=inline_start_list)


class Form(StatesGroup):
    referral_username = State()
    filter_start_price = State()
    filter_end_price = State()