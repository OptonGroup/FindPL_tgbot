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

import datetime 
from classes.product_key import ProductKeyManager



town_translate = {'москва': 'moskva', 'санкт-петербург': 'sankt-peterburg', 'новосибирск': 'novosibirsk', 'екатеринбург': 'ekaterinburg', 'казань': 'kazan', 'нижний новгород': 'nizhniy_novgorod', 'красноярск': 'krasnoyarsk', 'челябинск': 'chelyabinsk', 'самара': 'samara', 'уфа': 'ufa', 'ростов-на-дону': 'rostov-na-donu', 'краснодар': 'krasnodar', 'moskva': 'москва', 'sankt-peterburg': 'санкт-петербуг', 'novosibirsk': 'новосибирск', 'ekaterinburg': 'екатеринбург', 'kazan': 'казань', 'nizhniy_novgorod': 'нижний новгород', 'krasnoyarsk': 'красноярск', 'chelyabinsk': 'челябинск', 'samara': 'самара', 'ufa': 'уфа', 'rostov-na-donu': 'ростов-на-дону', 'krasnodar': 'краснодар'}
product_key_manager = ProductKeyManager()


async def identification_user(message: Message, state: FSMContext) -> None:
    is_user_in_chanel = await check_sub_on_chanel(message=message)
    if not is_user_in_chanel:
        return
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
            ref_data = user_info[10],
            filter_start_price = user_info[11],
            filter_end_price = user_info[12],
            last_active = user_info[13]
        )
        
async def check_sub_on_chanel(message) -> bool:
    user_status = await bot.get_chat_member(chat_id=-1002080804090, user_id=message.from_user.id)
    if user_status.status == 'left':
        await message.answer(
            'Доступ к боту доступен только пользователям, подписанным на наш тг канал @kvm_tg'
        )
        return False
    return True
            
       
async def start_work_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await identification_user(message=callback_query, state=state)
    await bot.answer_callback_query(callback_query.id)
    
    
    await bot.send_message(callback_query.from_user.id, 'Работа бота Возобновлена ✅')
    
    
        

async def buy_sub_handler(message: Message, state: FSMContext) -> None:
    is_user_in_chanel = await check_sub_on_chanel(message=message)
    if not is_user_in_chanel:
        return
    await identification_user(message=message, state=state)
    await message.answer('Чтобы настроить <b>фильтры</b> - оформите <b>подписку за Telegram Stars</b> ⭐️\n<b>Фильтр</b> поможет вам настроить ценовой диапазон, это сильно упростит поиск нужной квартиры\n\nВы можете приобрести звезды через @PremiumBot')
    
    sub_price = 200
    user_info = await state.get_data()
    if user_info['ref_activated']:
        sub_price = 150
    
    await message.answer_invoice(
            title="Фильтры доступны по подписке",
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
    is_user_in_chanel = await check_sub_on_chanel(message=message)
    if not is_user_in_chanel:
        return
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
    is_user_in_chanel = await check_sub_on_chanel(message=message)
    if not is_user_in_chanel:
        return
    await message.answer(
        f"Выберите город для поиска",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Москва"),
                    KeyboardButton(text="Санкт-Петербург"),
                    KeyboardButton(text="Новосибирск"),
                ],
                [
                    KeyboardButton(text="Екатеринбург"),
                    KeyboardButton(text="Казань"),
                    KeyboardButton(text="Нижний Новгород"),
                ],
                [
                    KeyboardButton(text="Красноярск"),
                    KeyboardButton(text="Челябинск"),
                    KeyboardButton(text="Самара"),
                ],
                [
                    KeyboardButton(text="Уфа"),
                    KeyboardButton(text="Ростов-на-Дону"),
                    KeyboardButton(text="Краснодар"),
                ]
            ],
            resize_keyboard=True,
        )
    )
    
    
async def change_town_handler(message: Message, state: FSMContext) -> None:
    is_user_in_chanel = await check_sub_on_chanel(message=message)
    if not is_user_in_chanel:
        return
    await identification_user(message=message, state=state)
    database.user_change_city(tg_id=message.from_user.id, town=town_translate[message.text.lower()])
    await message.answer(
        f'Город поиска квартир изменён на {message.text}',
        reply_markup=components.keyboard
    )
    

async def price_filter_handler(message: Message, state: FSMContext) -> None:
    is_user_in_chanel = await check_sub_on_chanel(message=message)
    if not is_user_in_chanel:
        return
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    end_sub = datetime.datetime.strptime(user_info['sub_end'], '%Y-%m-%d %H:%M:%S')
    
    if datetime.datetime.now().now() < end_sub:
        await message.answer(
            'Введите <b>число</b>, без учета залога и лишних трат - <b>только ежемесячный платеж</b>\n\n<b>Минимальная</b> стоимость аренды:',
            reply_markup=components.reset_button
        )
        await state.set_state(components.Form.filter_start_price)
    else:
        await message.answer('Чтобы настроить <b>фильтры</b> - оформите <b>подписку за Telegram Stars</b> ⭐️\n\n<b>Фильтр</b> поможет вам настроить ценовой диапазон, это сильно упростит поиск нужной квартиры')
        sub_price = 200
        user_info = await state.get_data()
        if user_info['ref_activated']:
            sub_price = 150
        
        await message.answer_invoice(
                title="Фильтры доступны по подписке",
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
        
        
async def reset_filter(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    database.user_change_filter_price(tg_id=callback_query.from_user.id, from_price=0, to_price=int(1e6))
    await identification_user(message=callback_query, state=state)
    user_info = await state.get_data()
    await bot.send_message(callback_query.from_user.id, f'Теперь вы получаете уведомления о появлении новых квартир в ценовом диапазоне <code>от {user_info["filter_start_price"]} до {user_info["filter_end_price"]} рублей</code>')
    await state.clear()
    
    

async def price_filter_min(message: Message, state: FSMContext):
    min_price = message.text
    
    if min_price.isdigit():
        database.user_change_filter_price(tg_id=message.from_user.id, from_price=min_price)
        await message.answer('<b>Максимальная</b> стоимость аренды:')
        await state.set_state(components.Form.filter_end_price)
    else:
        await message.answer(
            'Введите <b>число</b>, без учета залога и лишних трат - <b>только ежемесячный платеж</b>\n\n<b>Минимальная</b> стоимость аренды:',
            reply_markup=components.reset_button    
        )
        await state.set_state(components.Form.filter_start_price)
        

async def price_filter_max(message: Message, state: FSMContext):
    max_price = message.text
    
    if max_price.isdigit():
        database.user_change_filter_price(tg_id=message.from_user.id, to_price=max_price)
        await identification_user(message=message, state=state)
        user_info = await state.get_data()
        await message.answer(f'Теперь вы получаете уведомления о появлении новых квартир в ценовом диапазоне <code>от {user_info["filter_start_price"]} до {user_info["filter_end_price"]} рублей</code>')
        await state.clear()
    else:
        await message.answer('<b>Максимальная</b> стоимость аренды:')
        await state.set_state(components.Form.filter_end_price)


async def process_callback_button_key(callback_query: CallbackQuery, state: FSMContext):
    await identification_user(message=callback_query, state=state)
    await bot.answer_callback_query(callback_query.id)
    
    user_info = await state.get_data()
    
    await bot.send_message(callback_query.from_user.id, 'Введите свой ключ продукта:')
    await state.set_state(components.Form.product_key)


async def process_product_key(message: Message, state: FSMContext):
    await identification_user(message=message, state=state)
    key = message.text
    username = message.from_user.username or str(message.from_user.id)
    
    if product_key_manager.activate_key(key, username):
        database.user_renew_subscription(message.from_user.id, 0)
        await message.answer("Ключ введён верно. Доступ активрован")
    else:
        await message.answer("Неправильный ключ. Попробуйте ещё раз или обратитесь к агенту у которого покупали ключ")