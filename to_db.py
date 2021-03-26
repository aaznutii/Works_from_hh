"""
https://office-menu.ru/python/96-api-hh
"""
# Библиотека для анализа данных, представляющая данные в табличном виде называемом DataFrame
# Вся мощь данной библиотеки нам здесь не понадобиться, с ее помощью мы положим
# данные в БД. Можно было бы написать простые insert-ы
import pandas as pd

# Импортируем модуль вывода jupyter
# from IPython import display

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
id_employers = []  # Список с id работодателей

# Создаем списки для столбцов таблицы skills
skills_vac = []  # Список идентификаторов вакансий
skills_name = []  # Список названий навыков

#
# В выводе будем отображать прогресс
# Для этого узнаем общее количество файлов, которые надо обработать
# Счетчик обработанных файлов установим в ноль
cnt_docs = len(os.listdir('./from_hh/docs/vacancies/'))
i = 0

# Проходимся по всем файлам в папке vacancies
for fl in os.listdir(r'C:\Users\aaznu\Works_from_hh\from_hh\docs\vacancies/'):

    # Открываем, читаем и закрываем файл
    f = open('./from_hh/docs/vacancies/{}'.format(fl), encoding='utf8')
    json_text = f.read()
    f.close()

    # Текст файла переводим в справочник
    json_obj = json.loads(json_text)

    # Заполняем списки для таблиц
    ids.append(json_obj['id'])
    names.append(json_obj['name'])
    descriptions.append(json_obj['description'])
    id_employers.append('employer')

    # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
    for skl in json_obj['key_skills']:
        skills_vac.append(json_obj['id'])
        skills_name.append(skl['name'])

    # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
    i += 1
    # display.clear_output(wait=True)
    # display.display(tuple('Готово {} из {}'.format(i, cnt_docs)))
    print('Готово {} из {}'.format(i, cnt_docs))

passvd = int('Введите пароль')
# Создадим соединение с БД
eng = sql.create_engine('postgresql://{postgres}:' + f'{passvd}' + '@{127.0.0.1}:{5432}/{hh}')
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
