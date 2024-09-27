from core.parser.get_rate import Parser

def main(first_currency:str='USD', second_currency:str='RUB'):
    pars = Parser()
    result = pars.get_currency_rate(first_currency, second_currency)

if __name__=='__main__':
    main()