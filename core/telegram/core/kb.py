from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json
import numpy as np

def generate_menu(level:str):
    
    with open('/home/pmonk-1487/projects/trader/core/telegram/config/buttom_menu_all/buttom.json', encoding='utf-8') as f:
        menu_json = json.load(f)
        
    builder = InlineKeyboardBuilder()
    for i in range(len(menu_json[level]['callback_data'])):
        builder.button(
            text=menu_json[level]['text'][i], 
            callback_data=menu_json[level]['callback_data'][i])
    builder.adjust(1)
    return builder

def generate_menu_rate(text_arr, callback_data_arr):
            
    builder = InlineKeyboardBuilder()
    text_arr = np.append(text_arr, 'Обратно в меню!')
    callback_data_arr = np.append(callback_data_arr, 'menu')
    for i in range(text_arr.shape[0]):
        builder.button(
            text=text_arr[i], 
            callback_data=callback_data_arr[i])
    builder.adjust(1)
    return builder

def home_menu():
    return  [
        [InlineKeyboardButton(text="Добавить тренировку", callback_data="how_work_for_your")],
        [InlineKeyboardButton(text="Удалить тренировку", callback_data="how_work_for_client")],
        [InlineKeyboardButton(text="Узнать загруженность", callback_data="buy")]
    ]

menu_int_client = [
    [InlineKeyboardButton(text="Расскажи", callback_data="tell_me")],
    [InlineKeyboardButton(text="Покажи", callback_data="show_me")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]
menu = InlineKeyboardMarkup(inline_keyboard=home_menu())
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
cource_exit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="course")], 
                                                       [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])