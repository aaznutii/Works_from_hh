"""
https://office-menu.ru/python/96-api-hh
"""
# Библиотека для анализа данных, представляющая данные в табличном виде называемом DataFrame
# Вся мощь данной библиотеки нам здесь не понадобиться, с ее помощью мы положим
# данные в БД. Можно было бы написать простые insert-ы
import pandas as pd

import json
import os
from datetime import date

# Для удаления тегов
from lxml import html

# Фиксируем дату обращения
now = date.today().strftime("%d-%m-%Y")


# Создаем списки для столбцов таблицы vacancies
ids = []  # Список идентификаторов вакансий
names = []  # Список наименований вакансий
descriptions = []  # Список описаний вакансий
id_employers = []  # Список с id работодателей
prof_name = []     # Список наименований профессий (ключевые слова поиска)

spec_vac = []   # Список идентификаторов вакансий
spec_name_vac = []    # Название вакансии
spec_id_employers = []  #   Код работодателя
spec_profarea = []       # Прфессиональная сфера
spec_name = []    # Специализация

# Создаем списки для столбцов таблицы skills
skills_vac = []  # Список идентификаторов вакансий
skills_name = []  # Список названий навыков
skills_prof = []  # Список названий выборки профессий

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
        # Очищаем описание вакансии от тегов
        good_descript = html.fromstring(json_obj['description']).text_content()
        # Заполняем списки для таблиц
        ids.append(json_obj['id'])
        names.append(json_obj['name'])
        descriptions.append(good_descript)
        id_employers.append(json_obj['employer'])
        prof_name.append(json_obj['name_vac'])

        # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом.
        for skl in json_obj['key_skills']:
            # Для обхода ошибки получения данных по ключу при получении имени  и id проверяем равенство списка
            if len([json_obj['id'], json_obj['name_vac'], skl['name']]) == 3:
                skills_vac.append(json_obj['id'])
                skills_prof.append(json_obj['name_vac'])
                skill = str(skl['name']).lower()
                skills_name.append(skill)
            else:
                with open('log.txt', 'a', encoding='utf-8') as f:
                    skl_err = f'Ошибка заполнения данных для таблицы skills. Файл: {fl}\n'
                    f.write(skl_err)

        for el in json_obj['specializations']:
            spec_vac.append(json_obj['id'])
            spec_name_vac.append(json_obj['name'])
            spec_id_employers.append(json_obj['employer'])
            spec_name.append(el['name'])

        # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
        i += 1
    except UnicodeDecodeError:
        print('Ошибка чтения файла')
        data_err = os.path.basename(fl)
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(data_err)
        continue

    print('Готово {} из {}'.format(i, cnt_docs))


# Создаем пандосовский датафрейм, который затем сохраняем в БД в таблицу vacancies
df = pd.DataFrame({'id': ids, 'name': names, 'description': descriptions,
                   'id_employers': id_employers, 'prof_name': prof_name, 'date': now})
# df['date'] = now
df.to_csv(f'from_hh/result/hh_vacancies.csv', mode='a')
# Для удобства сохраняю на рабочий стол
df.to_excel(f'/Users/aaznu/Desktop/hh_vacancies.xlsx')

# Тоже самое, но для таблицы skills
df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name, 'prof': skills_prof, 'date': now})
df.to_csv(f'from_hh/result/hh_skills.csv', mode='a')
# Для удобства сохраняю на рабочий стол
df.to_excel(f'/Users/aaznu/Desktop/hh_skills.xlsx')

# Тоже самое, но для таблицы spec
df = pd.DataFrame({'vacancy': spec_vac, 'spec_name_vac': spec_name_vac,
                   'id_empl': spec_id_employers, 'skill': spec_name, 'date': now})
df.to_csv(f'from_hh/result/hh_spec.csv', mode='a')
# Для удобства сохраняю на рабочий стол
df.to_excel(f'/Users/aaznu/Desktop/hh_spec.xlsx')
