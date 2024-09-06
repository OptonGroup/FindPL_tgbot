from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from dblogic.database import database

from botlogic.settings import bot
from botlogic import components

import logging
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
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
            town_search = user_info[7],
            ref_activated = user_info[8],
            ref_voted = user_info[9],
            ref_data = user_info[10]
        )
        
        
        

async def buy_sub_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    await message.answer('Оплата через Telegram Stars ⭐️\n\nВы можете приобрести звезды через @PremiumBot')
    
    sub_price = 750
    user_info = await state.get_data()
    if user_info['ref_activated']:
        sub_price = 350
    
    await message.answer_invoice(
            title="Подписка на бота",
            description="Активация подписки на 1 месяц",
            currency="XTR",
            is_flexible=False,
            prices=[
                types.LabeledPrice(
                    label="Подписка на 1 месяц",
                    amount=sub_price
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
        amount=message.successful_payment.total_amount
    )
    if user_info['ref_activated']:
       database.user_del_ref(tg_id=user_info['tg_id'])
    
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    
    await message.answer(
        f"Платеж на сумму {message.successful_payment.total_amount} {message.successful_payment.currency} прошел успешно.\nВаша подписка продлена до <code>{user_info['sub_end']}</code>",
        reply_markup=components.keyboard
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
        reply_markup=components.keyboard
    )


async def process_callback_button_ref(callback_query: CallbackQuery, state: FSMContext):
    await identification_user(message=callback_query, state=state)
    await bot.answer_callback_query(callback_query.id)
    
    user_info = await state.get_data()
    if user_info['ref_voted']:
        await bot.send_message(callback_query.from_user.id, 'Вы уже вводили данные своего друга')
        return
    
    await bot.send_message(callback_query.from_user.id, 'Вводить username или 🔑 ID друга. username нужно вводить текстом без @. 🔑 ID вводить только числом')
    await state.set_state(components.Form.referral_username)
    
    
async def capture_referral_username(message: Message, state: FSMContext):
    referral = message.text
    
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    if referral.isdigit():
        if len(database.get_users(tg_id=referral, sub_active=True)):
            await message.answer(
                f'''Пользователь найден.\nСтоимость подписки изменена.'''
            )
            database.user_set_ref(tg_id=user_info['tg_id'], ref=referral)
            
        else:
            await message.answer(
                f'''Пользователь с ID={referral} не найден или у пользователя не активна подписка\nВвести данные друга вы сможете ещё раз по команде /start'''
            )
    else:
        if len(database.get_users(username=referral, sub_active=True)):
            await message.answer(
                f'''Пользователь найден.\nСтоимость подписки изменена.'''
            )
            database.user_set_ref(tg_id=user_info['tg_id'], ref=referral)
            
        else:
            await message.answer(
                f'''Пользователь с username={referral} не найден или у пользователя не активна подписка\nВвести данные друга вы сможете ещё раз по команде /start'''
            )

    await state.clear()
