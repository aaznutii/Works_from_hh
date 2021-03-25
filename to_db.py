"""
https://office-menu.ru/python/96-api-hh
"""
# Библиотека для анализа данных, представляющая данные в табличном виде называемом DataFrame
# Вся мощь данной библиотеки нам здесь не понадобиться, с ее помощью мы положим
# данные в БД. Можно было бы написать простые insert-ы
import pandas as pd

import json
import os

# Библиотека для работы с СУБД
from sqlalchemy import engine as sql

# Модуль для работы с отображением вывода Jupyter
from IPython import display

# Создаем списки для столбцов таблицы vacancies
ids = []  # Список идентификаторов вакансий
names = []  # Список наименований вакансий
descriptions = []  # Список описаний вакансий

# Создаем списки для столбцов таблицы skills
skills_vac = []  # Список идентификаторов вакансий
skills_name = []  # Список названий навыков

# В выводе будем отображать прогресс
# Для этого узнаем общее количество файлов, которые надо обработать
# Счетчик обработанных файлов установим в ноль
cnt_docs = len(os.listdir('./docs/vacancies'))
i = 0

# Проходимся по всем файлам в папке vacancies
for fl in os.listdir('./docs/vacancies'):

    # Открываем, читаем и закрываем файл
    f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
    jsonText = f.read()
    f.close()

    # Текст файла переводим в справочник
    jsonObj = json.loads(jsonText)

    # Заполняем списки для таблиц
    ids.append(jsonObj['id'])
    names.append(jsonObj['name'])
    descriptions.append(jsonObj['description'])

    # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
    for skl in jsonObj['key_skills']:
        skills_vac.append(jsonObj['id'])
        skills_name.append(skl['name'])

    # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
    i += 1
    display.clear_output(wait=True)
    display.display(tuple('Готово {} из {}'.format(i, cnt_docs)))

# Создадим соединение с БД
eng = sql.create_engine('postgresql://{Пользователь}:{Пароль}@{Сервер}:{Port}/{База данных}')
conn = eng.connect()

# Создаем пандосовский датафрейм, который затем сохраняем в БД в таблицу vacancies
df = pd.DataFrame({'id': ids, 'name': names, 'description': descriptions})
df.to_sql('vacancies', conn, schema='public', if_exists='append', index=False)

# Тоже самое, но для таблицы skills
df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
df.to_sql('skills', conn, schema='public', if_exists='append', index=False)

# Закрываем соединение с БД
conn.close()

# Выводим сообщение об окончании программы
display.clear_output(wait=True)
display.display(tuple('Вакансии загружены в БД'))
