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
            KeyboardButton(text="⭐️ Подписка"),
        ],
        [
            KeyboardButton(text="🏙 Город"),
            KeyboardButton(text="💬 Помощь"),
        ],
        [
            KeyboardButton(text="⚙️ Фильтр"),
        ]
    ],
    resize_keyboard=True
)


inline_start_list = [
    [InlineKeyboardButton(text="Ввести username друга", callback_data='add_referral')],
]
start_button = InlineKeyboardMarkup(inline_keyboard=inline_start_list)

inline_reset_list = [
    [InlineKeyboardButton(text="Сбросить", callback_data='reset_filter')],
]
reset_button = InlineKeyboardMarkup(inline_keyboard=inline_reset_list)

start_work_list = [
    [InlineKeyboardButton(text="Возобновить работу", callback_data='start_work')],
]
start_work_button = InlineKeyboardMarkup(inline_keyboard=start_work_list)


class Form(StatesGroup):
    referral_username = State()
    filter_start_price = State()
    filter_end_price = State()