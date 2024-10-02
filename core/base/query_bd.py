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