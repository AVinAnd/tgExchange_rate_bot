import requests
import json
from config import keys


class APIException(Exception):
    pass


class Price:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException('Указаны одинаковые валюты.')

        if float(amount) <= 0:
            raise APIException(f'Не удалось обработать количество "{amount}".')

        try:
            keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}".')

        try:
            keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}".')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}".')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        price = json.loads(r.content)[keys[quote]] * amount
        return price
