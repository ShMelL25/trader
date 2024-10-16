from aiogram import types, F, Router, flags, Dispatcher
from aiogram.types import Message, InputFile, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message,
)
from aiogram.fsm.state import State, StatesGroup

import config.text as text
from core.kb import generate_menu, iexit_kb
from .query_base.query_bd_get import Sql_Pars

router = Router()

class SaveMessage(StatesGroup):
    waiting_for_message = State()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=generate_menu(level='0').as_markup())
    await msg.delete()

@router.callback_query(lambda callback: callback.data == "registr")
async def register_handler(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    telegram_name = callback.from_user.full_name
    
    # Регистрируем пользователя, передавая имя и ID
    ret = Sql_Pars().register_user(telegram_name=telegram_name, telegram_id=telegram_id)
    await callback.message.answer(ret, reply_markup=generate_menu(level='2.1').as_markup())
    await callback.message.delete()

@router.callback_query(lambda callback: callback.data == "course")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    
    ret = Sql_Pars().get_rate(telegram_id=callback.from_user.id)
    
    await state.set_state(SaveMessage.waiting_for_message)
    await callback.message.answer('text.menu_train_edit', reply_markup=ret.as_markup())
    await callback.message.delete()

@router.callback_query(lambda callback: "rate" in callback.data)
async def add_handler(callback: CallbackQuery, state: FSMContext):
    
    
    pair = callback.data
    Sql_Pars().get_rate(pair=pair.split('_')[0], telegram_id=callback.from_user.id)
    print(pair.split('_')[0])
    photo_path = f'/home/pmonk-1487/projects/trader/core/telegram/log/{callback.from_user.id}.png'
    photo_file = FSInputFile(photo_path)
    await callback.message.reply_photo(photo=photo_file, reply_markup=iexit_kb)
    #await callback.message.answer('text.menu_train_edit', reply_markup=)
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "del_train")
async def del_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'saved_message' in data:
        #ret = SQL_request().del_train(text=data['saved_message'], telegram_id=callback.message.from_user.id)
        await callback.message.answer('Test', reply_markup=generate_menu(level='2.1').as_markup())
        
    else:
        await callback.message.answer("Вы ничего не добавляли!\nПопробуйте еще раз", reply_markup=generate_menu(level='2.1').as_markup())
    await state.clear()
    await callback.message.delete()   
    
@router.message(SaveMessage.waiting_for_message)
async def save_message(message: Message, state: FSMContext):
    data = await state.get_data()
    data['saved_message'] = message.text
    await state.update_data(data)
    await message.delete()
    
@router.callback_query(lambda callback: callback.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.message.answer(text.greet, reply_markup=generate_menu(level='0').as_markup())
    await callback.message.delete()