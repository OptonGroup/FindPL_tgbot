from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from dblogic.database import database

from botlogic.settings import bot
from botlogic.components import keyboard

import logging

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
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

town_translate = {'москва': 'moskva', 'moskva': 'москва', 'санкт-петербург': 'sankt-peterburg', 'sankt-peterburg': 'санкт-петербург', 'екатеринбург': 'ekaterinburg', 'ekaterinburg': 'екатеринбург', 'краснодар': 'krasnodar', 'krasnodar': 'краснодар'}



async def identification_user(message: Message, state: FSMContext) -> None:
    state_info = await state.get_data()
    if state_info.get('id', 0) != message.from_user.id:
        user_info = database.add_user(tg_id=message.from_user.id, username=message.from_user.username)
        await state.update_data(
            id = user_info[0],
            tg_id = user_info[1],
            username = user_info[2],
            is_admin = user_info[3],
            sub_start = user_info[4],
            sub_end = user_info[5],
            pay_money = user_info[6],
            town_search = user_info[7]
        )
        
        
        

async def buy_sub_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
        
    await message.answer_invoice(
            title="Подписка на бота",
            description="Активация подписки на бота на 1 месяц",
            provider_token="390540012:LIVE:55144",
            currency="rub",
            is_flexible=False,
            prices=[
                types.LabeledPrice(
                    label="Подписка на 1 месяц",
                    amount=1300*100
                )
            ],
            start_parameter="one-month-subscription",
            payload="test-invoice-payload"
    )
    
    
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    

async def successful_payment_handler(message: Message, state: FSMContext) -> None:
    logging.info(f'SUCCESSFUL PAYMENT: tg_id={message.from_user.id}')

    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    database.user_renew_subscription(
        tg_id=user_info['tg_id'],
        amount=message.successful_payment.total_amount // 100
    )
    
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    
    await message.answer(
        f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно.\nВаша подписка продлена до <code>{user_info['sub_end']}</code>",
        reply_markup=keyboard
    )
    
    

async def get_town_keyboard_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Выберите город для поиска",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Москва"),
                    KeyboardButton(text="Санкт-Петербург"),
                ],
                [
                    KeyboardButton(text="Екатеринбург"),
                    KeyboardButton(text="Краснодар"),
                ]
            ],
            resize_keyboard=True,
        )
    )
    
    
async def change_town_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    database.user_change_city(tg_id=message.from_user.id, town=town_translate[message.text.lower()])
    await message.answer(
        f'Город поиска квартир изменён на {message.text}',
        reply_markup=keyboard
    )
