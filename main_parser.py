from core.parser.get_rate import Parser
from multiprocess.pool import ThreadPool

def main():
    currancy_arr = Parser()._get_currency()
    print(currancy_arr)
    arr_ = []
    with ThreadPool(len(currancy_arr[0])) as p:
        for i in p.starmap(get_main, zip(currancy_arr[0], currancy_arr[1])):
            arr_.append(i)
    
def get_main(first_currency:str, second_currency:str):
    pars = Parser()
    result = pars.get_currency_rate(first_currency, second_currency)
    print(result)
    return result

if __name__=='__main__':
    main()