# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os




def get_page(page=0, name=None):

    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
    if name is None:
        name = 'Аналитик'
    else:
    # Справочник для параметров GET-запроса
        params = {
            'text': f'NAME:{name}',  # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': 1586,  # Поиск ощуществляется по вакансиям Самарская область
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data


# Считываем первые 2000 вакансий
def get_pages(path, name):
    for page in range(0, 20):
        # Преобразуем текст ответа запроса в справочник Python
        js_obj = json.loads(get_page(page, name))

    # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
    # Определяем количество файлов в папке для сохранения документа с ответом запроса
    # Полученное значение используем для формирования имени документа
        next_file_name = f'{path}{len(os.listdir(path))}.json'

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(next_file_name, mode='w', encoding='utf8')
        f.write(json.dumps(js_obj, ensure_ascii=False))
        f.close()

        # Проверка на последнюю страницу, если вакансий меньше 2000
        if (js_obj['pages'] - page) <= 1:
            break

        # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 3 сек мы можем подождать
        time.sleep(3)
    print(f'Старницы поиска собраны для вакансии: {name}')


def get_data(path_get_pages, path_get_vacancies):
    # Создаем список id организаций
    employers_id = []
    count = 0
    # Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле
    for fl in os.listdir(path_get_pages):
        # Открываем файл, читаем его содержимое, закрываем файл
        f = open('{}{}'.format(path_get_pages, fl), encoding='utf8')
        json_text = f.read()
        f.close()

        # Преобразуем полученный текст в объект справочника
        json_obj = json.loads(json_text)

        if count % 50 == 0:
            time.sleep(4)

        # Получаем и проходимся по непосредственно списку вакансий
        for v in json_obj['items']:
            count += 1
            # Обращаемся к API и получаем детальную информацию по конкретной вакансии
            req_vacancie = requests.get(v['url'])
            data_vacancie = req_vacancie.content.decode()
            data = json.loads(data_vacancie)
            #  Добавляем в словарь id компании-нанимателя
            try:
                data["employer"] = v["employer"]["id"]
            except KeyError:
                data["employer"] = None

            # #  Добавляем в словарь ключевые компетенции по вакансии
            # req_specializations = requests.get(f'https://api.hh.ru/vacancies/{v["id"]}')
            # data_specializations = req_specializations.content.decode()
            # data_spec = json.loads(data_specializations)
            # try:
            #     data["key_skills"] = data_spec['key_skills']
            # except KeyError:
            #     data["key_skills"] = None

            data = json.dumps(data, ensure_ascii=False)
            req_vacancie.close()

            # Создаем файл в формате json с идентификатором вакансии в качестве названия
            # Записываем в него ответ запроса и закрываем файл
            file_name = f"{path_get_vacancies}{v['id']}.json"
            f = open(file_name, mode='w', encoding='utf8')
            f.write(data)
            f.close()
            # time.sleep(3)
    # with open('from_hh/docs/employers_id.json', 'w', encoding='utf-8' ) as f:
    #     f.write(json.dumps(set(employers_id), ensure_ascii=False))

    print(f'Вакансий собрано: {count}')
    print(f'Идентификаторов работодателей записано: {len(set(employers_id))}')


def main():
    path_get_pages = r'C:\Users\aaznu\Works_from_hh\from_hh\docs\pagination/'
    path_get_vacancies = r'C:\Users\aaznu\Works_from_hh\from_hh\docs\vacancies/'

    names = ['Аналитик', 'Программист', 'Педагог', 'Учитель', 'Воспитатель', 'Химик', 'Социалный работник',
             'Инженер', 'Сварщик', 'Психолог', 'Переводчик', 'Электрик', 'Социолог', 'Няня', 'Документовед',
             'Делопроизводитель', 'Секретарь', 'Копирайтер', 'Редактор', 'СММ', 'Корректор',
             'Системный администратор']

    for name in names:
        get_pages(path_get_pages, name)
    get_data(path_get_pages, path_get_vacancies)


if __name__ == '__main__':
    main()
