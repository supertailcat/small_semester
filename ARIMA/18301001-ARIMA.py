import matplotlib.pyplot as plt
import pandas as pd
import statsmodels
import seaborn as sns
import statsmodels.tsa.api as smt
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

plt.rcParams['figure.figsize'] = [20, 6] # 图的长度

# 画图
weather_sets = pd.read_csv("alldaydata.csv", parse_dates=['date']) # 将'date'项转为日期
# 将日期设置为index
weather_sets = weather_sets.set_index('date')
# test：提取数据
# sentiment_short = weather_sets.loc['2000-01-01':'2001-01-01']
# print(type(sentiment_short))

# x = weather_sets['date']
# y1 = weather_sets['tmax']
# y2, y3 = weather_sets['tmin'], weather_sets['avg']
# plt.plot(x, y1, label='tmax')
#
# plt.xlabel('Date')
# plt.ylabel('Temperature')
# plt.title('Forecast')
#
# # plt.legend()
# # plt.show()
#
#
# 取时间片段
sentiment_short = weather_sets.loc['1980-01-01':'1981-01-01']
# 取平均气温
sentiment_short = sentiment_short.loc[:, ['avg']]
sentiment_short.plot(figsize=(20, 6))

plt.title("Consumer Sentiment")
plt.show()

# # 差分法生成一阶、二阶差分
# sentiment_short['diff_1'] = sentiment_short['avg'].diff(1)
# # sentiment_short['diff_1'] = sentiment_short['diff_1'].truncate(brfore=ym[1])
# sentiment_short['diff_2'] = sentiment_short['diff_1'].diff(1) # 二阶
# # sentiment_short.plot(subplots=True, figsize=(18, 12))
# # plt.show()
#
#
# # ARIMA模型
# del sentiment_short['diff_2']
# del sentiment_short['diff_1']
# # print(sentiment_short.head())

# 差分处理
D_sentiment_short = sentiment_short.diff().dropna()


def tsplot(y, lags=None, title='', figsize=(14, 8)):
    fig = plt.figure(figsize=figsize)
    layout = (2, 2)
    ts_ax = plt.subplot2grid(layout, (0, 0))
    hist_ax = plt.subplot2grid(layout, (0, 1))
    acf_ax = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    y.plot(ax=hist_ax, kind='hist', bins=25)
    hist_ax.set_title('Histogram')
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    # sns.despine()
    plt.tight_layout()
    plt.show()
    return ts_ax, acf_ax, pacf_ax


tsplot(D_sentiment_short, title='Consumer Sentiment', lags=36)

# 平稳性检测
from statsmodels.tsa.stattools import adfuller as ADF
# 返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
print(u'原始序列的ADF检验结果为：', ADF(sentiment_short['avg']))
# 白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox
print(u'差分序列的白噪声检验结果为：', acorr_ljungbox(sentiment_short, lags=1))  # 返回统计量和p值

# 定阶
sentiment_short['avg'] = sentiment_short['avg'].astype(float)
pmax = int(len(D_sentiment_short)/10)  # 一般阶数不超过length/10
qmax = int(len(D_sentiment_short)/10)  # 一般阶数不超过length/10
bic_matrix = []  # BIC矩阵
for p in range(pmax+1):
  tmp = []
  for q in range(qmax+1):
    try:  # 存在部分报错，所以用try来跳过报错。
      tmp.append(ARIMA(sentiment_short, (p,1,q)).fit().bic)
    except:
      tmp.append(None)
  bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值

p,q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置。
print(u'BIC最小的p值和q值为：%s、%s' %(p,q))


# ARIMA模型
model = ARIMA(sentiment_short, order=(1, 0, 0))
results = model.fit()
resid = results.resid #赋值
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40)
plt.show()

# 检验
model = sm.tsa.ARIMA(sentiment_short, order=(1, 0, 1))
results = model.fit()
predict_sunspots = results.predict(start='1980-01-01', end='1981-01-01', dynamic=False)
# print(predict_sunspots)
fig, ax = plt.subplots(figsize=(12, 8))
ax = sentiment_short.plot(ax=ax)
predict_sunspots.plot(ax=ax)

results.forecast(1)
plt.show()


