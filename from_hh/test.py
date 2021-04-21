import pandas as pd
import matplotlib

df = pd.read_csv(r'C:\Users\aaznu\Works_from_hh\from_hh\result\hh_skills.csv')
column = ['Unnamed: 0', 'vacancy', 'skill', 'prof', 'date']
viev_skl = df.groupby('prof')['skill'].value_counts()
# viev_skl.query('')
print(viev_skl)
