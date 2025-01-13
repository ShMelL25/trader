from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config import config
import pandas as pd
import numpy as np
from ..kb import generate_menu_rate
from .create_img import create_rate_plot_plolty, pie_plot_create

class Sql_Pars(object):
    
    def __init__(self):
        self.engine = create_engine(config.SQL_URL)
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
                        
    def add_transaction(self, sum_tr:float, telegram_id:int, type_tr:str):
        
        sum_tr = float(sum_tr)
        id_user = self.get_id(telegram_id=telegram_id)
            
        if id_user == None:
            return 'None'
        
        query_add = f'''
                INSERT INTO enrolment_expenses (user_id, sum_enrolment_expenses, type_transaction) 
                VALUES ({id_user},{sum_tr}, '{type_tr}')
            '''
        self.session.execute(text(query_add))
        self.session.commit()
        self.session.close()   
        
    def get_date_year_moth(self, telegram_id):
        
        query = f"""
            select 	
			to_char(t1.date_enrolment, 'YYYY-MM') as year_month
            from enrolment_expenses t1 
            join users_trade_torch t3 on t3.id = t1.user_id
            where telegram_id = {telegram_id}
            group by
			to_char(t1.date_enrolment, 'YYYY-MM')
        
        """
        df = pd.read_sql(query, self.engine)
        
        if len(df) >= 1:
            df['year_month_name_t'] = df['year_month']+'_date'
                
            return generate_menu_rate(text_arr=df['year_month'].to_numpy(), callback_data_arr=df['year_month_name_t'])

        return 'Данных нет'
        
    
    def get_transaction(self, telegram_id, date_add):
        query = f"""
            select 	
			to_char(t1.date_enrolment, 'YYYY-MM') as year_month,
            t3.telegram_id,
            t1.type_transaction,
            sum(t1.sum_enrolment_expenses) as sum_enrolment_expenses
            from enrolment_expenses t1 
            join users_trade_torch t3 on t3.id = t1.user_id
            where t3.telegram_id = {telegram_id} and to_char(t1.date_enrolment, 'YYYY-MM') = '{date_add}'
			
            group by
			to_char(t1.date_enrolment, 'YYYY-MM'),
            t3.telegram_id,
            t1.type_transaction
        
        """
        df = pd.read_sql(query, self.engine)
        
        txt_json = {
            'enrolment':'Доходы',
            'expenses':'Расходы',
        }
        
        for name in df['type_transaction'].unique():
            df.loc[(df['type_transaction'] == name), 'type_transaction'] = txt_json[name]
        pie_plot_create(df, telegram_id)
        
    
    def get_id(self, telegram_id):
        query_get = f'''select * 
                    from users_trade_torch
                    where telegram_id = {telegram_id}
                    '''
        if pd.read_sql(query_get, self.engine).shape[0] < 1:
            
            return 'None'
        
        else:
            return pd.read_sql(query_get, self.engine)['id'].to_numpy()[0]