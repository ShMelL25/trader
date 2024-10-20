import re
from bs4 import BeautifulSoup
from datetime import datetime
from ..base.query_bd import _get_currency_pairs, _add_currency_pairs, _add_currency_rate, _get_currency_list
import pandas as pd
import numpy as np
import requests
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Parser(object):
    
    def __init__(self):
        self.get_currency_rate
        self.engine = create_engine('postgresql://postgres:Santaclausoffice6@192.168.31.230:5432/trade_bd')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
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
        self.add_database_data(result, f'{first_currency}/{second_currency}', second_currency)
        
        # Возвращаем курс валюты как число
        return result
        
    def add_database_data(self, current:float, current_name:str, currency_name:str):
        
        df_pairs = pd.read_sql(_get_currency_pairs(current_name), self.engine)
        if df_pairs.shape[0]==0:
            
            self.session.execute(_add_currency_pairs(current_name))
            self.session.commit()    
            df_pairs = pd.read_sql(_get_currency_pairs(current_name), self.engine)
        
        self.session.execute(_add_currency_rate(df_pairs['id'].to_numpy()[0], current, datetime.now()))
        self.session.commit()
        self.session.close()
        
    def _get_currency(self):
        
        df = pd.read_sql(_get_currency_list(), self.engine)
        
        return [list(df['base_currency'].to_numpy()), list(df['quote_currency'].to_numpy())]