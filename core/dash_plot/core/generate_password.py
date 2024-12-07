from random import choice
import bcrypt
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd

class Password:
    
    def __init__(self):
        self.symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&*+-=?@^_'
        self.engine = create_engine(config.SQL_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def create_new_password(self):
        password = ''
        for i in range(16):
            password += choice(self.symbols)
            
        return password
    
    def hash_password(self, password:str)->bytes:
        
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        
    def check_password(self, 
                       password:str, 
                       hashAndSalt:bytes)->bool:
        
        return bcrypt.checkpw(password.encode(), hashAndSalt)
    
    def add_bd_password(self, telegram_id:int, hashAndSalt:bytes):

        id_user = self.get_id(telegram_id)
        
        if id_user == None:
            return 'None'
        
        query_add = f'''
                INSERT INTO user_dash_board (user_id, password) 
                VALUES ({id_user},{hashAndSalt})
            '''
        self.session.execute(text(query_add))
        self.session.commit()
        self.session.close()  
        
    def get_id(self, telegram_id):
        query_get = f'''select * 
                    from users_trade_torch
                    where telegram_id = {telegram_id}
                    '''
        if pd.read_sql(query_get, self.engine).shape[0] < 1:
            
            return 'None'
        
        else:
            return pd.read_sql(query_get, self.engine)['id'].to_numpy()[0]
    
    