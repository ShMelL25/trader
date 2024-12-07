from aiogram import types, F, Router, flags, Dispatcher
from aiogram.types import Message, InputFile, FSInputFile
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message,
)
from aiogram.fsm.state import State, StatesGroup

from ..config import text
from ..core.kb import generate_menu, iexit_kb, cource_exit_kb
from .query_base.query_bd_get import Sql_Pars
from .query_base.create_img import del_img

from ...dash_plot.core.generate_password import Password

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
    await callback.message.answer(ret, reply_markup=iexit_kb)
    await callback.message.delete()

@router.callback_query(lambda callback: callback.data == "course")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    
    ret = Sql_Pars().get_rate(telegram_id=callback.from_user.id)
    
    await state.set_state(SaveMessage.waiting_for_message)
    await callback.message.answer('text.menu_train_edit', reply_markup=ret.as_markup())
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "expenses_receipts")
async def train_handler(callback: CallbackQuery):
    await callback.message.answer(text.info_expenses_receipts, reply_markup=generate_menu(level='0.1').as_markup())
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "add_")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    await state.set_state(SaveMessage.waiting_for_message)
    await callback.message.answer(text.add_test, reply_markup=generate_menu(level='1').as_markup())
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "get_")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    await state.set_state(SaveMessage.waiting_for_message)
    
    date_menu = Sql_Pars().get_date_year_moth(callback.from_user.id)
    
    if type(date_menu) != str:
        #await callback.message.reply_photo(photo=FSInputFile(f'/home/pmonk-1487/projects/trader/core/telegram/log/{callback.from_user.id}.png'), 
                                        #reply_markup=iexit_kb)
        #del_img(callback.from_user.id)
        await callback.message.answer(text.date_info, reply_markup=date_menu.as_markup())
        await callback.message.delete()
    else:
        await callback.message.answer(date_menu, reply_markup=iexit_kb)
        await callback.message.delete()
    
@router.callback_query(lambda callback: "date" in callback.data)
async def add_handler(callback: CallbackQuery, state: FSMContext):
    
    date_get = callback.data
    ret = Sql_Pars().get_transaction(date_add=date_get.split('_')[0], telegram_id=callback.from_user.id)
    await callback.message.reply_photo(photo=FSInputFile(f'/home/pmonk-1487/projects/trader/core/telegram/log/{callback.from_user.id}.png'), 
                                       reply_markup=iexit_kb)
    del_img(callback.from_user.id)
    await callback.message.delete()

@router.callback_query(lambda callback: "rate" in callback.data)
async def add_handler(callback: CallbackQuery, state: FSMContext):
    
    pair = callback.data
    ret = Sql_Pars().get_rate(pair=pair.split('_')[0], telegram_id=callback.from_user.id)
    await callback.message.reply_photo(photo=FSInputFile(f'/home/pmonk-1487/projects/trader/core/telegram/log/{callback.from_user.id}.png'), 
                                       reply_markup=cource_exit_kb, caption=f"{pair.split('_')[0]}: {ret}")
    del_img(callback.from_user.id)
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "expenses")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    saved_message = data.get('saved_message', 'No message has been saved yet.')
    Sql_Pars().add_transaction(saved_message,callback.from_user.id,'expenses')

    # Отправляем сохраненное сообщение пользователю
    await callback.message.answer(saved_message, reply_markup=iexit_kb)
    #await callback.message.answer('text.menu_train_edit')
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "receipts")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    
    data = await state.get_data()
    saved_message = data.get('saved_message', 'No message has been saved yet.')
    Sql_Pars().add_transaction(saved_message,callback.from_user.id,'enrolment')

    # Отправляем сохраненное сообщение пользователю
    await callback.message.answer(saved_message, reply_markup=iexit_kb)
    #await callback.message.answer('text.menu_train_edit')
    await callback.message.delete()
    
@router.callback_query(lambda callback: callback.data == "dash_board")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    
    Password()
    # Отправляем сохраненное сообщение пользователю
    await callback.message.answer(text.return_url(), reply_markup=generate_menu(level='0.2').as_markup())
    #await callback.message.answer('text.menu_train_edit')
    await callback.message.delete()
    
@router.message(StateFilter(SaveMessage.waiting_for_message))
async def save_message(message: types.Message, state: FSMContext):
    # Сохраняем сообщение в данные состояния
    await state.update_data(saved_message=message.text)
    #await message.reply("Your message has been saved!")

    # Удаляем сообщение
    try:
        await message.delete()
    except Exception as e:
        #print(f"Failed to delete message: {e}")
        pass
    
@router.callback_query(lambda callback: callback.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.message.answer(text.greet, reply_markup=generate_menu(level='0').as_markup())
    await callback.message.delete()