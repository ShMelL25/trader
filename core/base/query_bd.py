import datetime
from sqlalchemy import text

def _get_currency_pairs(current_name:str)->str:
    return text(f"""SELECT id 
        FROM currency_pairs
        WHERE pair_name = '{current_name}'
        """)
        
def _add_currency_pairs(current_name:str)->str:
    
    cur_arr = current_name.split('/')
    query = text(f"""
            INSERT INTO currency_pairs (pair_name, base_currency, quote_currency)
            VALUES ('{current_name}', '{cur_arr[0]}', '{cur_arr[1]}')""")
            
    return query

def _add_currency_rate(currency_pair_id:int, exchange_rate:float, date:datetime.datetime)->str:
    
    query = text(f"""
            INSERT INTO currency_rate (currency_pair_id, exchange_rate, date)
            VALUES ({currency_pair_id}, {exchange_rate}, '{str(date)}')""")
    print(query)      
    return query


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