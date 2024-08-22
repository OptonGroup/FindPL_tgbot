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
from botlogic.components import keyboard



async def secret_code_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    user_info = await state.get_data()
    database.user_set_admin(tg_id=user_info['tg_id'], is_admin=1)
        
    await message.answer(
        'Теперь Вы - Админ. Доступные вам комманды на /admin_commands',
        reply_markup=keyboard
    )
    

async def admin_commands_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
        
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
        
    await message.answer(
        'Вы - Админ. Доступные комманды:\n/get_admin_25634 - Получить права админа\n/admin_commands - Получить команды, доступные админам\n/get_user_by_id [user_id] - Получить информацию о пользователе по его [🔑ID]\n/get_user_by_name [username] - Получить информацию о пользователе по его [Имя Пользователя]\n/give_admin [user_id] - Выдать прова админа пользователю по его [🔑ID]\n/remove_admin [user_id] - Забрать права админа пользователя по его [🔑ID]\n/get_users_info - Получить информацию о всех пользователях\n/get_logs - Получить лог файл бота\n/give_sub [user_id] - Выдать подписку пользователю на неделю по его [🔑ID]',
        reply_markup=keyboard
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
    if not user_info['is_admin']:
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=keyboard
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
            reply_markup=keyboard
        ) 
    except:
        await message.answer(
            f'Пользователь с id={user_id} не найден',
            reply_markup=keyboard
        )
        

async def get_user_by_username_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
    
    username = command.args
    if not username:
        await message.answer(
            'Необходимо ввести [Имя пользователя]. Напимер /get_user_by_name durov',
            reply_markup=keyboard
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
            reply_markup=keyboard
            
        ) 
    except:
        await message.answer(
            f'Пользователь с username={username} не найден',
            reply_markup=keyboard
        )


async def give_admin_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=keyboard
        )
        return
    
    try:
        database.user_set_admin(tg_id=user_id, is_admin=1)
        await message.answer(
            f'Админ-права были выданы пользователю id={user_id}',
            reply_markup=keyboard
        )
    except:
        await message.answer(
            f'Не получилось выдать Админ-права пользователю id={user_id}',
            reply_markup=keyboard
        )
        

async def remove_admin_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=keyboard
        )
        return
    
    try:
        database.user_set_admin(tg_id=user_id, is_admin=0)
        await message.answer(
            f'Забрали Админ-права у пользователя id={user_id}',
            reply_markup=keyboard
        )
    except:
        await message.answer(
            f'Не получилось забрать Админ-права у пользователя id={user_id}',
            reply_markup=keyboard
        )
        

async def get_users_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
    
    data = []
    for row in database.get_users():
        data.append([element for element in row])
    head = ['id', 'tg_id', 'username', 'is_admin', 'sub_start', 'sub_end', 'pay_money', 'town_search']
         
    with open('files/users_info.txt', 'w', encoding='utf-8') as file:
        file.write(tabulate(data, headers=head, tablefmt="grid"))
    document = FSInputFile('files/users_info.txt')
    await message.answer_document(document, reply_markup=keyboard)
    document = ''
    

async def get_logs_handler(message: Message, state: FSMContext) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
    
    document = FSInputFile('info.log')
    await message.answer_document(document, reply_markup=keyboard)
    document = ''
    
    
async def give_sub_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
    await identification_user(message=message, state=state)
    
    user_info = await state.get_data()
    if not user_info['is_admin']:
        return
    
    user_id = command.args
    if not user_id:
        await message.answer(
            'Необходимо ввести [🔑ID] пользователя. Напимер /get_user_by_id 123456789',
            reply_markup=keyboard
        )
        return
    
    try:
        database.user_renew_subscription(tg_id=user_id, amount=0)
        await message.answer(
            f'Продлили подписку у пользователя id={user_id} на месяц',
            reply_markup=keyboard
        )
    except:
        await message.answer(
            f'Не получилось продлить подписку у пользователя id={user_id}',
            reply_markup=keyboard
        )
