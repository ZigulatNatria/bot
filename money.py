import json
import requests


class ConvertionException(Exception): # Класс исключений (ошибок)
    pass


class Converter:   # Основной класс
    @staticmethod
    def get_price():

        r = requests.get('https://free.currconv.com/api/v7/convert?q=USD_RUB,RUB_USD&compact=ultra&apiKey=648d49b34a55105e76fb')
        rq = json.loads(r.content) # Преобразуем ответ в JSON

        return rq['USD_RUB']
        # return print(rq)

Converter.get_price()