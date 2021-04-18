# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Библиотека для сохранения в csv - Для создания справочника работодателей
import pandas as pd

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os

# регулярные выражения
import re

# Генератор случайных чисел
import random

"""['Лаборант', 'Юрист', 'Юристконсульт', 'Фотограф', 'Журналист', 'Оператор', 'SMM', 'Аналитик',
         'Программист', 'Педагог', 'Учитель', 'Воспитатель', 'Химик', 'Социалный работник', 'Социолог', 'Инженер',
         'Сварщик', 'Психолог', 'Переводчик', 'Электрик', 'Социолог', 'Няня', 'Документовед', 'Делопроизводитель',
         'Секретарь', 'Копирайтер', 'Редактор', 'СММ', 'Корректор', 'Системный администратор', 'ЧПУ', 'Наладчик',
         'Технолог', 'SEO', 'Специалист', 'Менеджер', 'Логист', 'Экскурсовод', 'HR']"""

names = []


def get_page(page=0, name=None):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
    if name is None:
        name = '*'
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
        next_file_name = f'{path}{len(os.listdir(path))}_{name}.json'

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
    df_employers = {'id': [], 'name': [], 'name_vac': []}
    count = 0
    # Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле
    for fl in os.listdir(path_get_pages):
        # забираем имя вакансии
        name_vac = ''.join(re.findall(r'[^\d_.json]', os.path.basename(fl)))

        # Открываем файл, читаем его содержимое, закрываем файл
        f = open('{}{}'.format(path_get_pages, fl), encoding='utf8')
        json_text = f.read()
        f.close()

        # Преобразуем полученный текст в объект справочника
        json_obj = json.loads(json_text)

        # Делаем паузу в обращениях через каждые 50 запросов.
        if count % 50 == 0:
            time.sleep(3)

        # Получаем и проходимся непосредственно по списку вакансий
        for v in json_obj['items']:
            except_count = 0
            """
            Попытка получить данные по 'url' с учетом прерывания доступа.
            """
            # Обращаемся к API и получаем детальную информацию по конкретной вакансии
            try:
                os.listdir(path_get_pages)
                req_vacancie = requests.get(v['url'])
                data_vacancie = req_vacancie.content.decode()
                data = json.loads(data_vacancie)
                data['name_vac'] = name_vac
                #  Добавляем в основной словарь  id компаний-нанимателей. Формирует словарь компаний
                try:
                    data["employer"] = v["employer"]["id"]
                    df_employers['id'].append(v["employer"]["id"])
                    df_employers['name'].append(v["employer"]["name"])
                    df_employers['name_vac'].append(name_vac)
                except KeyError:
                    data["employer"] = "None"
                    df_employers['id'].append("None")
                    df_employers['name'].append("None")
                    df_employers['name_vac'].append(name_vac)
                data = json.dumps(data, ensure_ascii=False)
                req_vacancie.close()
                # Создаем файл в формате json с идентификатором вакансии в качестве названия
                # Записываем в него ответ запроса и закрываем файл
                file_name = f"{path_get_vacancies}{v['id']}.json"
                f = open(file_name, mode='w', encoding='utf8')
                f.write(data)
                print(f'Файл создан: {file_name} для вакансии {name_vac}')
                f.close()
                count += 1
            except ConnectionError:
                if except_count < 10:
                    pause = random.randrange(2, 6)
                    print(f'Ошибка доступа к файлу. Программа установлена на паузу: {pause} секунд.')
                    except_count += 1
                    time.sleep(pause)
                else:
                    break
    # Преобразуем словарь в датафрейм и сохраняем в csv
    df = pd.DataFrame(df_employers)
    df.to_csv(r'C:\Users\aaznu\Works_from_hh\from_hh\result\hh_employers.csv', mode='a')
    print(f'Вакансий собрано: {count}')


# def get_vacancies():


def main():
    path_get_pages = r'C:\Users\aaznu\Works_from_hh\from_hh\docs\pagination/'
    path_get_vacancies = r'C:\Users\aaznu\Works_from_hh\from_hh\docs\vacancies/'
    # for name in set(names):
    #     get_pages(path_get_pages, name)
    get_data(path_get_pages, path_get_vacancies)


if __name__ == '__main__':
    main()
