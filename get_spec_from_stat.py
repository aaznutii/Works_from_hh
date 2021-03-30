# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json


def get_specializations():
    """
    Загрузка по api  и создание перечня специализаций
    """
    req = requests.get('https://api.hh.ru/salary_statistics/dictionaries/professional_areas')  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    js_obj = json.loads(data)
    print(js_obj)
    f = open('from_hh/docs/spec_from_stat.json', mode='w', encoding='utf8')
    f.write(json.dumps(js_obj, ensure_ascii=False))
    f.close()


def get_spec_list():
    """
    Создание списка специализаций
    """
    f = open("from_hh/docs/spec_from_stat.json", encoding='utf8')
    json_text = f.read()
    f.close()
    json_data = json.loads(json_text)

    specializations = []

    for profarea_name in json_data:
        for el in profarea_name['specializations']:
            specializations.append(el['name'])

    with open('from_hh/docs/spec_from_vac.txt', 'a', encoding='utf-8') as file:
        for el in specializations:
            el = el+'\n'
            file.write(el)


def main():
    get_specializations()
    # get_spec_list()


if __name__ == '__main__':
    main()
