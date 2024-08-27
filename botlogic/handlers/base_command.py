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
        f'''<b>Что может делать этот бот?</b>\nБот FindPL уведомляет обо всех новых объявлениях на площадке Авито о снятии квартир в городах  Москва, Санкт-Петербург, Екатеринбург, Краснодар.\nВам доступна подписка до <code>{user_info['sub_end']}</code>''',
        reply_markup=keyboard
    )
    

async def get_info_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    user_info_text = f'''ℹ️ Профиль\n- - - - - - - - - - - - - - - - - - - - - - - -\n\n🕑 Подписка до <code>{user_info['sub_end']}</code>\n🌆Город поиска: <code>{town_translate[user_info['town_search']].capitalize()}</code>\n🔑 ID: <code>{user_info['tg_id']}</code>\n▫️ Username: <code>{user_info['username']}</code>\n\n- - - - - - - - - - - - - - - - - - - - - - - -'''
    await message.answer(user_info_text, reply_markup=keyboard)
    

async def support_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        '''
О нашем сервисе:
1. С помощью нашего бота вы сможете оперативно дозваниваться до собственников, благодаря чему вы сможете быть первым в очереди на просмотр.

2. Некоторые риэлторы тоже дозваниваются первыми через аналогичный сервис, далее выставляют квартиры уже с комиссией. Наш бот поможет вам быть быстрее.

Цена услуг:
Стоимость подписки на наш сервис составляет 1300₽ в месяц.

Правила оформления и сроки исполнения заказа:
1. Подписка оформляется через Telegram-бота.
2. Уведомления начинают поступать сразу после оплаты подписки.
3. Подписка действует в течение 30 дней с момента оплаты.

Условия оплаты:
Оплата производится через сервис Robokassa, поддерживающий различные способы оплаты. После успешной оплаты подписка активируется автоматически.

Возврат и отказ от покупки:
Возврат средств возможен только в случае технической ошибки на стороне нашего сервиса, повлекшей неполучение услуг. Для возврата обратитесь в поддержку.

Самозанятый: Горлов Денис Юрьевич  
ИНН: 744843123600

Политика обработки персональных данных:
Мы соблюдаем все требования законодательства о защите персональных данных. Ваши данные используются только для предоставления услуг и не передаются третьим лицам.

Поддержка: @s1cptn
        ''',
        reply_markup=keyboard
    )
