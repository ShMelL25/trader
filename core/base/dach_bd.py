from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
import numpy as np
from config import config
from .query_bd import _get_user_id, _add_bd_password_query, \
            _get_bd_password_query, _change_password_query, \
            _get_transaction_query, get_date_year_moth_query,\
            get_type_query, _add_transaction_query
import bcrypt
from datetime import datetime


class Data_Base_Dash:
    
    def __init__(self):
        self.engine = create_engine(config.SQL_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()  
        
    def get_bd_password(self, telegram_id:int)->bytes|str:
        
        id_user = self.get_id(telegram_id)
        
        if id_user == 'None':
            return 'None_registr'
        
        df = pd.read_sql(_get_bd_password_query(id_user=id_user), self.engine)
        
        if len(df) < 1:
            return 'None'
        
        return df['password'].to_numpy()[-1].encode()
        

    def add_bd_password(self, telegram_id:int, hashAndSalt:bytes):

        id_user = self.get_id(telegram_id)
        
        if id_user == None:
            return 'None'
        
        query_add = _add_bd_password_query(id_user=id_user,
                                           hashAndSalt=hashAndSalt.decode())
        
        self.session.execute(text(query_add))
        self.session.commit()
        self.session.close()  
        
    def change_bd_password(self, telegram_id:int, hashAndSalt:bytes):

        id_user = self.get_id(telegram_id)
        
        if id_user == None:
            return 'None'
        
        query_add = _change_password_query(id_user=id_user,
                                           password=hashAndSalt.decode())
        
        self.session.execute(text(query_add))
        self.session.commit()
        self.session.close()  
        
    def check_now_date(self, telegram_id):
        df = self.get_date_transaction_dash(telegram_id)
        
        if '-'.join(str(datetime.now().date()).split('-')[:2]) not in df:
            query = _add_transaction_query(self.get_id(telegram_id=telegram_id), 
                                   sum_tr=0,
                                   type_tr='expenses')
            self.session.execute(text(query))
            self.session.commit()
            self.session.close()   
        
        
    def get_id(self, telegram_id):
        
        df = pd.read_sql(_get_user_id(telegram_id=telegram_id), self.engine)
        
        if df.shape[0] < 1:
            return 'None'
        else:
            return df['id'].to_numpy()[0]
        
    def get_transaction_dash(self, 
                             telegram_id, 
                             date_add=None)->pd.DataFrame:
        
        df = pd.read_sql(_get_transaction_query(telegram_id, date_add), self.engine)
        return df
    
    def get_date_transaction_dash(self, 
                             telegram_id)->np.array:
        
        df = pd.read_sql(get_date_year_moth_query(telegram_id), self.engine)
        
        return df.to_numpy()
    
    def get_type_transaction_dash(self, 
                             telegram_id)->np.array:
        
        df = pd.read_sql(get_type_query(telegram_id), self.engine)
        
        return df.to_numpy()
    
    def update_add_table(self, 
                     telegram_id:int, 
                     value:float,
                     type_transaction:str, 
                     text_expenses:str,
                     date_tr:str):
        
        id_ = self.get_id(telegram_id)
        
        if date_tr == None or date_tr == '':
            query = f"""INSERT INTO 
                                  enrolment_expenses (user_id, sum_enrolment_expenses, type_transaction, text_expenses) 
                                  VALUES ({id_}, {value}, '{type_transaction}', '{text_expenses}')
                                  """
        else:
            query = f"""INSERT INTO 
                                  enrolment_expenses (user_id, sum_enrolment_expenses, type_transaction, text_expenses, date_enrolment) 
                                  VALUES ({id_}, {value}, '{type_transaction}', '{text_expenses}', date('{date_tr}'))
                                  """
        
        self.session.execute(text(query))
        self.session.commit()
        self.session.close()
        
    def update_dell_table(self, id_):
        self.session.execute(text(f"""
                                  DELETE FROM enrolment_expenses WHERE id = {id_}
                                  """))
        
        self.session.commit()
        self.session.close()
    
    def close_connect(self):
        self.session.close()  