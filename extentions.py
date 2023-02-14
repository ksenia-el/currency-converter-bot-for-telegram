#  process input from user as 3 values: currency to buy, currency to pay, amount of purchase
#  also returns an exchange rate of 2 requested currencies

import json
import requests
from config import currencies, TOKEN


class CryptoConverter:
    @staticmethod
    def get_exchange_rate(exch_currency: str, base_currency: str, amount: str):

        #  processing inputs of currencies and amount from user (and handling errors in case of something go wrong)
        try:
            #  next line of code declares a ticker of base_currency from user inputs
            #  this ticker will be used then to make an API request
            base_currency_ticker = currencies[base_currency]
        #  but in case user entered invalid currency, then it will throw an error message
        except KeyError:
            raise UserException("Currency of payment doesn't exist\n\nTo check all currencies available use this command: /values\nOr use this command to try again: /try")

        try:
            exch_currency_ticker = currencies[exch_currency]
        except KeyError:
            raise UserException("Currency of purchase doesn't exist\n\nTo check all currencies available use this command: /values\nOr use this command to try again: /try")

        #  in case user entered the same currencies to buy and purchase
        if exch_currency == base_currency:
            raise UserException("Currencies of purchase and payment should be different\n\nUse this command to try again: /try")

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            raise UserException(f"Can't process your amount of currency to purchase ({amount}). It can't be zero or less\\nUse this command to try again: /try")

        #  in case everything was entered correctly
        #  by the next line of code we get an object with exchange rates of requested currencies
        curr_response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={exch_currency_ticker}&tsyms={base_currency_ticker}")
        response_content = json.loads(curr_response.content)
        # to get an exchange rate of base_currency from response - and record it in this variable
        exchange_rate = response_content[currencies[base_currency]]
        return exchange_rate


class UserException(Exception):
    pass
