from core.parser.get_rate import Parser

def main(first_currency, second_currency):
    pars = Parser()
    pars.get_currency_rate(first_currency, second_currency)