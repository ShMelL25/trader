from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config import config_telegram
import pandas as pd

class Sql_Pars(object):
    
    def __init__(self):
        self.engine = create_engine(config_telegram.SQL_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def register_user(self, telegram_id, telegram_name):
        
        query_get = f'''select telegram_id 
                    from users_trade_torch
                    where telegram_id = {telegram_id}
                    
                    '''
        if pd.read_sql(query_get, self.engine).shape[0] < 1:
            query_add = f'''
                INSERT INTO users_trade_torch (telegram_id, telegram_name) 
                VALUES ({telegram_id}, '{telegram_name}')
            '''
            self.session.execute(text(query_add))
            self.session.commit()
            self.session.close()
            
            return 'Рестрация прошла успешно!'
        
        
        return 'Вы уже зарегистрированы!'
        