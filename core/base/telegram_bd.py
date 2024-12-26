from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config import config
import pandas as pd
import numpy as np
from ..telegram.core.kb import generate_menu_rate
from ..telegram.core.query_base.create_img import create_rate_plot_plolty, pie_plot_create
from .query_bd import _get_telegram_user, _add_telegram_user, _get_currency_pairs, _get_currency_pairs_all, \
                    _get_currency_rate, _add_transaction_query, get_date_year_moth_query, _get_transaction_query, _get_user_id

class Sql_Pars:
    
    def __init__(self):
        self.engine = create_engine(config.SQL_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def register_user(self, telegram_id, telegram_name):
        query_get = _get_telegram_user(telegram_id=telegram_id)
        
        if pd.read_sql(query_get, self.engine).shape[0] < 1:
            query_add = _add_telegram_user(telegram_id=telegram_id, telegram_name=telegram_name)
            
            self.session.execute(text(query_add))
            self.session.commit()
            self.session.close()
            
            return 'Рестрация прошла успешно!'
        
        return 'Вы уже зарегистрированы!'
    
    def get_rate(self, telegram_id:int, pair:str=None):
        
        if pair == None:
            query_get = _get_currency_pairs_all()
            df = pd.read_sql(query_get, self.engine)
            df['pair_name_t'] = df['pair_name']+'_rate'
            
            return generate_menu_rate(text_arr=df['pair_name'].to_numpy(), callback_data_arr=df['pair_name_t'])
        
        else:
            query_get = _get_currency_rate(pair)
            
            df = pd.read_sql(query_get, self.engine)
            create_rate_plot_plolty(data=df, telegram_id=telegram_id)
            return df['rate'].to_numpy()[-1]
                        
    def add_transaction(self, sum_tr:float, telegram_id:int, type_tr:str):
        
        sum_tr = float(sum_tr)
        id_user = self.get_id(telegram_id=telegram_id)
            
        if id_user == None:
            return 'None'
        
        query_add = _add_transaction_query(id_user, sum_tr,type_tr)
        self.session.execute(text(query_add))
        self.session.commit()
        self.session.close()   
        
    def get_date_year_moth(self, telegram_id):
        
        query = get_date_year_moth_query(telegram_id)
        df = pd.read_sql(query, self.engine)
        
        if len(df) >= 1:
            df['year_month_name_t'] = df['year_month']+'_date'
                
            return generate_menu_rate(text_arr=df['year_month'].to_numpy(), callback_data_arr=df['year_month_name_t'])

        return 'Данных нет'
        
    
    def get_transaction(self, telegram_id, date_add):
        
        query = _get_transaction_query(telegram_id=telegram_id,
                                       date_add=date_add)
        
        df = pd.read_sql(query, self.engine)
        
        txt_json = {
            'enrolment':'Доходы',
            'expenses':'Расходы',
        }
        
        for name in df['type_transaction'].unique():
            df.loc[(df['type_transaction'] == name), 'type_transaction'] = txt_json[name]
        pie_plot_create(df, telegram_id)
        
    
    def get_id(self, telegram_id):
        
        query_get = _get_user_id(telegram_id)
        
        if pd.read_sql(query_get, self.engine).shape[0] < 1:
            
            return 'None'
        
        else:
            return pd.read_sql(query_get, self.engine)['id'].to_numpy()[0]
        
    def close_connect(self):
        self.session.close() 