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
    
    