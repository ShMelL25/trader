import re
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import os

class Parser(object):
    
    def __init__(self):
        self.get_currency_rate
    
    def get_currency_rate(self, first_currency, second_currency):
        # Адрес сайта, с которого мы будем получать данные
        url = f"https://www.google.com/search?q={first_currency}+to+{second_currency}+exchange+rate"
        
        # Получаем содержимое страницы
        response = requests.get(url)
        
        # Создаем объект BeautifulSoup для парсинга HTML-разметки
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Получаем элемент с курсом валюты
        result = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text()
        
        
        result = float('.'.join(re.findall("\d+", result)))
        self.create_data_frame(result, f'{first_currency}/{second_currency}', second_currency)
        
        # Возвращаем курс валюты как число
        return result
    
    def create_data_frame(self, current:float, current_name:str, currency_name:str):
        
        try:
            df_current = pd.read_csv('core/base/current.csv')
            df_f = pd.DataFrame(
                columns=['datetime', 'date', 'current_name', 'current', 'currency_name'],
                data = list(zip([datetime.now()], [datetime.now().date()], [current_name], [current], [currency_name]))
                )
            df_current = pd.concat([df_current, df_f])
        except FileNotFoundError:
            df_current = pd.DataFrame(
                columns=['datetime', 'date', 'current_name', 'current', 'currency_name'],
                data = list(zip([datetime.now()], [datetime.now().date()], [current_name], [current], [currency_name]))
                )
        df_current.to_csv('core/base/current.csv', index=False)