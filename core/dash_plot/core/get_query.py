from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ....config import config
import pandas as pd


class Dash_BD(object):
    
    def __init__(self):
        self.engine = create_engine(config.SQL_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    def get_user_info(self, info_user:dict)->bool:
        
        query = """
        
        """
        df = pd.read_sql(query, self.engine)
        
        if len(df) > 0:
            return True
        else:
            return False
        
    def add_user_info(self, telegram_id:int, info_user:dict)->bool:
        
        query = """
        
        """
        df = pd.read_sql(query, self.engine)
        
        if len(df) > 0:
            return True
        else:
            return False