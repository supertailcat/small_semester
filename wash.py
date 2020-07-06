import pandas as pd
from datetime import datetime
from dateutil import parser
data_raw = pd.read_csv('D:/weather/zhengzhou.csv',encoding='utf-8')
data_raw['date'] = data_raw['DATE'].apply(parser.parse)
data_raw['tmax'] = data_raw['TMAX'].astype(float)
data_raw['tmin'] = data_raw['TMIN'].astype(float)
data_raw['tavg'] = data_raw['TAVG'].astype(float)
data = data_raw.loc[:, ['date', 'tmax', 'tmin', 'tavg']]
data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin'])) & (pd.Series.notnull(data['tavg']))]
data = data[(data['date']>=datetime(1980, 1, 1))&(data['date']<=datetime(2020, 7, 1))]
data.to_csv('D:/weather/result/ZhengZhou.csv', index=None)
print('OK')