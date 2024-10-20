from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config import config_telegram
import pandas as pd
import numpy as np
from ..kb import generate_menu_rate
from .create_img import create_rate_plot_plolty

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
    
    def get_rate(self, telegram_id:int, pair:str=None):
        
        if pair == None:
            query_get = f'''select * 
                            from currency_pairs
                        
                        '''
            df = pd.read_sql(query_get, self.engine)
            df['pair_name_t'] = df['pair_name']+'_rate'
            
            return generate_menu_rate(text_arr=df['pair_name'].to_numpy(), callback_data_arr=df['pair_name_t'])
        
        else:
            query_get = f'''select 
                        date(t1.date),
                        t1.date as date_time,
                        max(t1.exchange_rate) as rate
                        from currency_rate t1
                        join currency_pairs t2 on t1.currency_pair_id=t2.id
                        where t2.pair_name = '{pair}'
                        group by
                        t1.date,
                        date(t1.date)
                        ORDER BY date(t1.date)
                        '''
            df = pd.read_sql(query_get, self.engine)
            create_rate_plot_plolty(data=df, telegram_id=telegram_id)
            return df['rate'].to_numpy()[-1]
                        
        