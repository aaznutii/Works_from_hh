"""
https://office-menu.ru/python/96-api-hh
"""
# Библиотека для анализа данных, представляющая данные в табличном виде называемом DataFrame
# Вся мощь данной библиотеки нам здесь не понадобиться, с ее помощью мы положим
# данные в БД. Можно было бы написать простые insert-ы
import pandas as pd

import re

# Импортируем модуль вывода jupyter
# from IPython import display

import json
import os
from datetime import date



# Создаем списки для столбцов таблицы vacancies
ids = []  # Список идентификаторов вакансий
names = []  # Список наименований вакансий
descriptions = []  # Список описаний вакансий
id_employers = []  # Список с id работодателей

spec_vac = []   # Список идентификаторов вакансий
spec_name_vac = []    # Название вакансии
spec_id_employers = []  #   Код работодателя
spec_profarea = []       # Прфессиональная сфера
spec_name = []    # Специализация

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

    try:
        # Открываем, читаем и закрываем файл
        f = open(f'./from_hh/docs/vacancies/{fl}', encoding='utf-8')
        json_text = f.read()
        f.close()

        # Текст файла переводим в справочник
        json_obj = json.loads(json_text)
        good_descript =json_obj['description']          #re.findall(r"А-я+", json_obj['description'])
        # Заполняем списки для таблиц
        ids.append(json_obj['id'])
        names.append(json_obj['name'])
        descriptions.append(good_descript)
        id_employers.append(json_obj['employer'])

        # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
        for skl in json_obj['key_skills']:
            skills_vac.append(json_obj['id'])
            skills_name.append(skl['name'])

        for el in json_obj['specializations']:
            spec_vac.append(json_obj['id'])
            spec_name_vac.append(json_obj['name'])
            spec_id_employers.append(json_obj['employer'])
            spec_name.append(el['name'])

        # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
        i += 1
    except UnicodeDecodeError:
        data_err = os.path.basename(fl)
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(data_err)
        continue
    except KeyError:
        continue
    print('Готово {} из {}'.format(i, cnt_docs))


# Фиксируем дату обращения для создания файла
now = date.today().strftime("%d%m%Y")

# Создаем пандосовский датафрейм, который затем сохраняем в БД в таблицу vacancies
df = pd.DataFrame({'id': ids, 'name': names, 'description': descriptions, 'id_employers': id_employers})
df.to_csv(f'from_hh/result/hh_vacancies_{now}.csv')
# # Для удобства сохраняю на рабочий стол
# df.to_csv(f'/Users/aaznu/Desktop/hh_vacancies_{now}.csv')

# Тоже самое, но для таблицы skills
df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
df.to_csv(f'from_hh/result/hh_skills_{now}.csv')

# Тоже самое, но для таблицы spec
df = pd.DataFrame({'vacancy': spec_vac, 'name_vac': spec_name_vac, 'id_empl': spec_id_employers, 'skill': spec_name})
df.to_csv(f'from_hh/result/hh_spec_{now}.csv')

#  Создаем файл с id работодателей
with open(f'./from_hh/docs/employers_id_{now}.', 'a', encoding='utf-8') as employers_file:
    for el in id_employers:
        if el is None:
            employers_file.write('None'+'\n')
        else:
            employers_file.write(el+'\n')
