from core.parser.get_rate import Parser
from multiprocess.pool import ThreadPool
import numpy as np

def main():
    currancy_arr = Parser()._get_currency()
    with ThreadPool(len(currancy_arr[0])) as p:
        p.starmap(get_main, zip(currancy_arr[0], currancy_arr[1]))
    
def get_main(first_currency:str, second_currency:str):
    pars = Parser()
    result = pars.get_currency_rate(first_currency, second_currency)

if __name__=='__main__':
    main()