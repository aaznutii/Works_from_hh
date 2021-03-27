# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os


def get_specializations():
    """
    Создаем метод для получения страницы со списком специализаций.
    """
    req = requests.get('https://api.hh.ru/specializations')  # Посылаем запрос к API
    # print(req)
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    js_obj = json.loads(data)
    print(js_obj)
    f = open('from_hh/docs/specializations.json', mode='w', encoding='utf8')
    f.write(json.dumps(js_obj, ensure_ascii=False))
    f.close()


# with open("from_hh/docs/vacancies/26864852.json") as json_file:
#     json_data = json.load(json_file)
#     print(json_data)

# get_specializations()
