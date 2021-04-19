import sqlalchemy

conn = sqlalchemy.create_engine('postgresql://{root}:{Пароль}@{localhost}:{Port}/{База данных}').connect()

import pandas as pd

# Загружаем наименования вакансий
# sql = 'select name from public.vacancies'
vacancies_name = pd.read_csv('from_hh/result/hh_vacancies_18042021.csv')

# Загружаем навыки по вакансиям
sql = """
    select
        v.name,
        skill
    from
        public.skills s
        join public.vacancies v
            on v.id = s.vacancy
"""

skills = pd.read_csv('from_hh/result/hh_skills.csv')

# Закрываем соединение с БД
# conn.close()

# sklearn - библиотека, содержащая набор инструментов для машинного обучения.
# feature_extraction.text извлекает признаки из текста, которые затем можно будет
# использовать в моделировании. В нашем случае моделирование не требуется. Нам нужно
# получить биграммы и их оценку
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

# Получим матрицу встрчаемости биграмм (токенов) для каждой вакансии
# В качестве стоп-слов установим грейды сотрудников, т.е. нам
# не важно Старший аналитик данных или Младший, нам важно, что он аналитик данных
# Также исключаем биграммы, которые встречаются реже, чем в 1-ой тысячной всех вакансий
cv = CountVectorizer(
    ngram_range=(2, 2),
    stop_words=['ведущий', 'главный', 'младший', 'эксперт', 'стажер', 'старший',
                'middle', 'junior', 'senior'],
    min_df=0.001
)
word_vector = cv.fit_transform(vacancies_name)

# Рассчитаем меру idf (обратная частота документа)
# Чем выше мера для конкретного токена, тем реже он встречается
idf = TfidfTransformer().fit(word_vector)

# Строим датафрейм с оценкой idf для каждого токена. Далее он понадобится для построения облака
df_idf = pd.DataFrame(idf.idf_, index=cv.get_feature_names(), columns=["idf"])

# Строим датафрейм из матрицы частоты токенов, где в качестве строк вакансии,
# токены в качестве столбцов. Далее используем его для получения списка вакансий, для
# которых встречается конкретный токен
pivot = pd.DataFrame(
    word_vector.toarray(),
    columns=cv.get_feature_names(),
    index=vacancies_name.values
)