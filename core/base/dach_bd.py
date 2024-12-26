from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
import numpy as np
from config import config
from .query_bd import _get_user_id, _add_bd_password_query, \
            _get_bd_password_query, _change_password_query, \
            _get_transaction_query, get_date_year_moth_query
import bcrypt


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
        
    def get_id(self, telegram_id):
        
        df = pd.read_sql(_get_user_id(telegram_id=telegram_id), self.engine)
        
        if df.shape[0] < 1:
            return 'None'
        else:
            return df['id'].to_numpy()[0]
        
    def get_transaction_dash(self, 
                             telegram_id, 
                             date_add)->pd.DataFrame:
        
        df = pd.read_sql(_get_transaction_query(telegram_id, date_add), self.engine)
        return df
    
    def get_date_transaction_dash(self, 
                             telegram_id)->np.array:
        
        df = pd.read_sql(get_date_year_moth_query(telegram_id), self.engine)
        
        return df.to_numpy()
        
    
    def close_connect(self):
        self.session.close()  