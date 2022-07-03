import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

data_csv = pd.read_csv('data.csv')
data = pd.DataFrame(data_csv)


######################################################
# Удаляем поврежденные строки (в 'Airport name' только латинские буквы, пробелы, тире, дефисы, скобки)

Backup = data

d = list(range(48, 58)) + list(range(65, 91)) + \
         list(range(97, 123)) + [45, 151, 40, 41, 32]


def check_name(line):
    for i in line:
        if ord(i) not in d:
            return False
            break
    return True


for i, j in data.iterrows():
    if check_name(j[0]) == False:
        data = data.drop(index=[i])
        # print(data.iloc[i])
# print(data.head())
# print(Backup)
###########################################################
# Поиск аэропортов, которые не приняли ни одного самолета за период 2007-2020

# Version 1
# data_7_20 = Backup[(Backup['Year'] > 2006) & (Backup['Year'] < 2021)]
# count_flies = data_7_20.pivot_table(
#     ['Whole year'], ['Airport name'], aggfunc='sum')
# count_null_flies = count_flies[count_flies['Whole year'] == 0]
# print(count_null_flies)

# Version 2
df = data.groupby('Airport name')[['January', 'February', 'March', 'April', 'May', 'June',
                                  'July', 'August', 'September', 'October', 'November', 'December', 'Whole year']].agg('sum')
df = df.reset_index()
df = df[df['Whole year'] == 0]
df = df.reset_index()

# В основной таблице только аэропорты, которые приимали суда в период с 2007-2020
data = data[data['Airport name'].isin(df['Airport name']) == False]

############################################################
# Найти аэропорты, которые прекратили принимать самолеты хотябы в один из годов: 2018-2020, при этом принимали суда до 2017 года

df_17 = data[data['Year'] <= 2017]
df_17 = df_17.groupby('Airport name')[['January', 'February', 'March', 'April', 'May', 'June',
                                      'July', 'August', 'September', 'October', 'November', 'December', 'Whole year']].agg('sum')
df_17 = df_17.reset_index()
df_17 = df_17[df_17['Whole year'] != 0]
# print(df_17.info())

df_18_0 = data[(data['Year'] == 2018) & (data['Whole year'] == 0)]
df_19_0 = data[(data['Year'] == 2019) & (data['Whole year'] == 0)]
df_20_0 = data[(data['Year'] == 2020) & (data['Whole year'] == 0)]

# df_18_1 = data[(data['Year'] == 2018) & (data['Whole year'] != 0)]
# df_19_1 = data[(data['Year'] == 2019) & (data['Whole year'] != 0)]
# df_20_1 = data[(data['Year'] == 2020) & (data['Whole year'] != 0)]

df_closed = df_17[
    (df_17['Airport name'].isin(df_18_0['Airport name']) == True)
    | (df_17['Airport name'].isin(df_19_0['Airport name']) == True)
    | (df_17['Airport name'].isin(df_20_0['Airport name']) == True)
]

# print(df_closed)
#############################################################################
# Исключить аэропорты, которые принимают более 5 млн людей в год (проблема с заданием), вывести топ 50 из оставшихся аэропортов, посчитать поток людей через все в сумме по каждому месяцу и найти амплитуду
big_airports = data[(data['Whole year'] >= 5*(10**6)) & (data['Year'] < 2020)
                    ]  # .groupby('Airport name')['Whole year'].agg(min).reset_index()

# В сортиторвке следующих данных учитывается 2020 год в потоке людей через аэропорты
new_data = data[(
    data['Airport name'].isin(set(big_airports['Airport name'])) == False)]

top_data = new_data.groupby('Airport name')[['January', 'February', 'March', 'April', 'May', 'June',
                                             'July', 'August', 'September', 'October', 'November', 'December', 'Whole year']].agg('sum').reset_index()

top_data = top_data.sort_values(
    by='Whole year', ascending=False).head(50).reset_index().drop(columns='index')

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

people_count = []
for month in months:
    people_count.append(top_data[month].sum())

# graphic = plt.plot(months, people_count)
# plt.grid(True)
# plt.show()
# print(max(people_count)-min(people_count))

#########################################################################
# из топ 50 (прошлая задача) выбрать топ 5 по процентному прирост потока людей между 2019 и 2007
# Проблемы: у некоторых аэропортов нет данных/данные == 0 по 2007/2019, всего рассматриваются не 50 аэропортов, а меньше
data_2007 = data[(data['Year'] == 2007) & (
    data['Airport name'].isin(top_data['Airport name']) == True)][['Airport name', 'Year', 'Whole year']].reset_index().drop(columns='index')

data_2019 = data[(data['Year'] == 2019) & (
    data['Airport name'].isin(top_data['Airport name']) == True)][['Airport name', 'Year', 'Whole year']].reset_index().drop(columns='index')

list_air = list(top_data['Airport name'])
list_values = []
data_2019 = data_2019.drop(index=46)

m_data = data_2019.merge(data_2007, on='Airport name')
m_data['diff'] = 0
for i in range(len(list(m_data['Airport name']))):
    n_2007 = float(m_data['Whole year_y'][i])
    n_2019 = float(m_data['Whole year_x'][i])
    if n_2007 == 0:
        m_data['diff'][i] = '0'
        continue
    m_data['diff'][i] = str((n_2019-n_2007)/n_2007)
m_data = m_data.sort_values(by='diff', ascending=False).head(
    5).reset_index().drop(columns='index')
print(m_data)
xx = list(m_data['Airport name'])
yy = list(m_data['diff'])
for i in range(5):
    yy[i] = float(yy[i])
print(xx)
print(yy)

graphic_top = plt.plot(xx, yy)
plt.grid(True)
plt.show()
