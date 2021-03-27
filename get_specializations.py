# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json


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


# get_specializations()


def get_spec_dict():
    f = open("from_hh/docs/specializations.json", encoding='utf8')
    json_text = f.read()
    f.close()
    json_data = json.loads(json_text)

    specializations = []

    for profarea_name in json_data:
        for el in profarea_name['specializations']:
            specializations.append(el['name'])
    print(specializations)


get_spec_dict()

# f = open('from_hh/docs/vacancies/32724608.json', encoding='utf8')
# json_text = f.read()
# f.close()
# json_obj = json.loads(json_text)
# for i, el in enumerate(json_obj):
#     print(f'{i}, {el}')



