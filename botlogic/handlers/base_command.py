from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from botlogic.handlers.database_command import identification_user
from botlogic import components

town_translate = {'москва': 'moskva', 'moskva': 'москва', 'санкт-петербург': 'sankt-peterburg', 'sankt-peterburg': 'санкт-петербург', 'екатеринбург': 'ekaterinburg', 'ekaterinburg': 'екатеринбург', 'краснодар': 'krasnodar', 'krasnodar': 'краснодар'}



async def command_start_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)

    user_info = await state.get_data()
    await message.answer(
        f'''<b>Получайте уведомления о появлении новых квартир -</b> дозванивайтесь первым, будьте первым в очереди на просмотр, арендуйте без комиссии\n\nМы доступны в 4 городах: Москва, Санкт-Петербург, Екатеринбург и Краснодар.\n\nВам доступна подписка до <code>{user_info['sub_end']}</code>''',
        reply_markup=components.keyboard
    )
    await message.answer(
        f'''<b>-53% на первый месяц 🔥</b>

Если у вашего друга активна подписка, вы можете ввести его username (если нет username, попросите друга его id из профиля бота)

Мы рады всем новым пользователям. Стоимость подписки по реферальной программе - 350 Telegram Stars ⭐️''',
        reply_markup=components.start_button
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
    await message.answer(user_info_text, reply_markup=components.keyboard)
    

async def support_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        '''
<b>Оплата через Telegram Stars ⭐️</b>

Вы можете приобрести звезды через @PremiumBot

<b>О нашем сервисе:</b>
С помощью нашего бота вы сможете оперативно дозваниваться до собственников, благодаря чему вы сможете быть первым в очереди на просмотр.

Некоторые риэлторы тоже дозваниваются первыми через аналогичный сервис, далее выставляют квартиры уже с комиссией. Наш бот поможет вам быть быстрее.

<b>Поддержка:</b> @s1cptn
        ''',
        reply_markup=components.keyboard
    )
