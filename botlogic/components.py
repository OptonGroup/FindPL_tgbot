from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

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
