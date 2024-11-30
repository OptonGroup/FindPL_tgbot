from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
from aiogram.types.input_file import FSInputFile

from dblogic.database import database

from botlogic.settings import bot

import logging
from tabulate import tabulate

from botlogic.handlers.base_command import identification_user
from botlogic import components
from classes.product_key import ProductKeyManager



async def secret_code_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    database.user_set_admin(tg_id=user_info['tg_id'], is_admin=1)
        
    await message.answer(
        'Теперь Вы - Админ. Доступные вам комманды на /admin_commands',
        reply_markup=components.keyboard
    )
    

async def admin_commands_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
        
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
        
    await message.answer(
        'Вы - Админ. Доступные комманды:\n/get_admin_25634 - Получить права админа\n/admin_commands - Получить команды, доступные админам\n/get_user_by_id [user_id] - Получить информацию о пользователе по его [🔑ID]\n/get_user_by_name [username] - Получить информацию о пользователе по его [Имя Пользователя]\n/give_admin [user_id] - Выдать прова админа пользователю по его [🔑ID]\n/remove_admin [user_id] - Забрать права админа пользователя по его [🔑ID]\n/get_users_info - Получить информацию о всех пользователях\n/get_logs - Получить лог файл бота\n/give_sub [user_id] - Выдать подписку пользователю на неделю по его [🔑ID]',
        reply_markup=components.keyboard
    )
    

async def process_user(user_info) -> dict:
    return {
        'id': user_info[0],
        'tg_id': user_info[1],
        'username': user_info[2],
        'is_admin': user_info[3],
        'sub_start': user_info[4],
        'sub_end': user_info[5],
        'pay_money': user_info[6],
        'town_search': user_info[7]
    }
    

async def get_user_by_id_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=components.keyboard
        )
        return
    
    try:
        user_info = database.get_user_by_tg_id(tg_id=user_id)
        user_info = await process_user(user_info)
        
        text = f'Информация о {user_id}\n'
        for row_name in user_info:
            text += f'<b>{row_name}</b> - {user_info[row_name]}\n'
        await message.answer(
            text,
            reply_markup=components.keyboard
        ) 
    except:
        await message.answer(
            f'Пользователь с id={user_id} не найден',
            reply_markup=components.keyboard
        )
        

async def get_user_by_username_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    username = command.args
    if not username:
        await message.answer(
            'Необходимо ввести [Имя пользователя]. Напимер /get_user_by_name durov',
            reply_markup=components.keyboard
        )
        return
    
    try:
        user_info = database.get_user_by_username(username=username)
        user_info = await process_user(user_info)
        
        text = f'Информация о {username}\n'
        for row_name in user_info:
            text += f'<b>{row_name}</b> - {user_info[row_name]}\n'
        await message.answer(
            text,
            reply_markup=components.keyboard
            
        ) 
    except:
        await message.answer(
            f'Пользователь с username={username} не найден',
            reply_markup=components.keyboard
        )


async def give_admin_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=components.keyboard
        )
        return
    
    try:
        database.user_set_admin(tg_id=user_id, is_admin=1)
        await message.answer(
            f'Админ-права были выданы пользователю id={user_id}',
            reply_markup=components.keyboard
        )
    except:
        await message.answer(
            f'Не получилось выдать Админ-права пользователю id={user_id}',
            reply_markup=components.keyboard
        )
        

async def remove_admin_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=components.keyboard
        )
        return
    
    try:
        database.user_set_admin(tg_id=user_id, is_admin=0)
        await message.answer(
            f'Забрали Админ-права у пользователя id={user_id}',
            reply_markup=components.keyboard
        )
    except:
        await message.answer(
            f'Не получилось забрать Админ-права у пользователя id={user_id}',
            reply_markup=components.keyboard
        )
        

async def get_users_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    data = []
    for row in database.get_users():
        data.append([element for element in row])
    head = ['id', 'tg_id', 'username', 'is_admin', 'sub_start', 'sub_end', 'pay_money', 'town_search', 'ref_activated', 'ref_voted', 'ref_data', 'filter_start_price', 'filter_end_price', 'last_active']
         
    with open('files/users_info.txt', 'w', encoding='utf-8') as file:
        file.write(tabulate(data, headers=head, tablefmt="grid"))
    document = FSInputFile('files/users_info.txt')
    await message.answer_document(document, reply_markup=components.keyboard)
    document = ''
    

async def get_logs_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    document = FSInputFile('info.log')
    await message.answer_document(document, reply_markup=components.keyboard)
    document = ''
    
    
async def give_sub_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=components.keyboard
        )
        return
    
    try:
        database.user_renew_subscription(tg_id=user_id, amount=0)
        await message.answer(
            f'Продлили подписку у пользователя id={user_id} на месяц',
            reply_markup=components.keyboard
        )
    except:
        await message.answer(
            f'Не получилось продлить подписку у пользователя id={user_id}',
            reply_markup=components.keyboard
        )

async def pass_test_com(message: Message, state: FSMContext) -> None:
    from botlogic.functions import functions
    
    await functions.send_text(text='Test')
    
    
    
product_key_manager = ProductKeyManager()

async def add_new_agent_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return

    if not command.args:
        await message.answer("Введите команду в формате: /add_new_agent [имя агента]")
        return

    agent_name = command.args
    try:
        filename = product_key_manager.create_agent_keys_file(agent_name)
        document = FSInputFile(filename)
        await message.answer_document(document, reply_markup=components.keyboard)
    except Exception as e:
        logging.error(f"Error generating product keys: {e}")
        await message.answer("Ошибка генерации ключей. Попробуйте позже")
        

async def get_keys_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    if not user_info.get('is_admin', False):
        return
    
    
    agent_name = command.args

    document = FSInputFile(f'agents/{agent_name}.json')
    await message.answer_document(document, reply_markup=components.keyboard)
    document = ''