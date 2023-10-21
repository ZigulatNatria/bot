import json
import requests
from config import api


class ConvertionException(Exception): # Класс исключений (ошибок)
    pass


class Converter:   # Основной класс
    @staticmethod
    def get_price():

        r = requests.get(api)    # Забираем данные с ресурса
        rq = json.loads(r.content) # Преобразуем ответ в JSON

        return rq['USD_RUB']      # Возвращаем только цену в рублях за доллар

Converter.get_price()