import datetime
from sqlalchemy import text

def _get_currency_pairs(current_name:str)->str:
    return text(f"""SELECT id 
        FROM currency_pairs
        WHERE pair_name = '{current_name}'
        """)
    
def _get_telegram_user(telegram_id:int)->str:
    return f'''select telegram_id 
                    from users_trade_torch
                    where telegram_id = {telegram_id}
                    
                    '''
                    
def _add_telegram_user(telegram_id:int, telegram_name:str)->str:
    return f'''
            INSERT INTO users_trade_torch (telegram_id, telegram_name) 
            VALUES ({telegram_id}, '{telegram_name}')
        '''
        
def _add_currency_pairs(current_name:str)->str:
    
    cur_arr = current_name.split('/')
    query = text(f"""
            INSERT INTO currency_pairs (pair_name, base_currency, quote_currency)
            VALUES ('{current_name}', '{cur_arr[0]}', '{cur_arr[1]}')""")
            
    return query

def _get_currency_pairs_all()->str:
    
    query = f'''select * 
                from currency_pairs
            '''
    return query

def _add_currency_rate(currency_pair_id:int, exchange_rate:float, date:datetime.datetime)->str:
    
    query = text(f"""
            INSERT INTO currency_rate (currency_pair_id, exchange_rate, date)
            VALUES ({currency_pair_id}, {exchange_rate}, '{str(date)}')""")
    print(query)      
    return query

def _get_currency_rate(pair)->str:
    
    query = f'''select 
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
    return query

def _add_transaction_query(id_user,
                           sum_tr,
                           type_tr):
    return f'''
                INSERT INTO enrolment_expenses (user_id, sum_enrolment_expenses, type_transaction) 
                VALUES ({id_user},{sum_tr}, '{type_tr}')
            '''
            
def _get_transaction_query(telegram_id,
                           date_add=None):
    
    if str(date_add) != 'None':
        return f"""
                select 	
                t1.id,
                to_char(t1.date_enrolment, 'YYYY-MM') as year_month,
                t3.telegram_id,
                t1.type_transaction,
                sum(t1.sum_enrolment_expenses) as sum_enrolment_expenses
                from enrolment_expenses t1 
                join users_trade_torch t3 on t3.id = t1.user_id
                where t3.telegram_id = {int(telegram_id)} and to_char(t1.date_enrolment, 'YYYY-MM') = '{date_add}'
                
                group by
                t1.id,
                to_char(t1.date_enrolment, 'YYYY-MM'),
                t3.telegram_id,
                t1.type_transaction
            
            """
            
    return f"""
                select 
                t1.id,	
                to_char(t1.date_enrolment, 'YYYY-MM') as year_month,
                t3.telegram_id,
                t1.type_transaction,
                sum(t1.sum_enrolment_expenses) as sum_enrolment_expenses
                from enrolment_expenses t1 
                join users_trade_torch t3 on t3.id = t1.user_id
                where t3.telegram_id = {int(telegram_id)}
                
                group by
                t1.id,
                to_char(t1.date_enrolment, 'YYYY-MM'),
                t3.telegram_id,
                t1.type_transaction
            
            """
            
def get_date_year_moth_query(telegram_id):
    return f"""
            select 	
			to_char(t1.date_enrolment, 'YYYY-MM') as year_month
            from enrolment_expenses t1 
            join users_trade_torch t3 on t3.id = t1.user_id
            where telegram_id = {int(telegram_id)}
            group by
			to_char(t1.date_enrolment, 'YYYY-MM')
        
        """

def _get_currency_list()->str:
    
    query = text(f"select base_currency, quote_currency from currency_pairs")     
    return query

def _get_user_id(telegram_id:int)->str:
    query_get = f'''select id
                    from users_trade_torch
                    where telegram_id = {telegram_id}
                    '''
    return query_get

def _change_password_query(id_user:int, password:str)->str:
    query_get = f'''UPDATE user_dash_board
                    SET password = '{password}',
                    date_create = '{str(datetime.datetime.now())}'
                    WHERE user_id = {id_user}
                '''
    return query_get

def _get_bd_password_query(id_user:int):
    
    return f"""
                select *
                from user_dash_board
                where user_id = {id_user}
            """

def _add_bd_password_query(id_user:int, hashAndSalt:str):
    
    return f'''
                INSERT INTO user_dash_board (user_id, password, date_create) 
                VALUES ({id_user},'{hashAndSalt}', '{str(datetime.datetime.now())}')
            '''