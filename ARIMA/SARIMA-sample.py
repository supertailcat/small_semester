# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:34:26 2020

@author: 94763
"""
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
 
def Sarima(station):
    data = pd.read_csv("D:/weather/result/"+station+".csv",parse_dates=['date'],index_col='date')

    data=data['tavg'].resample('D').mean()
    data=data.fillna(data.bfill())
    data.plot(figsize=(30,6)) #图大小长宽
    plt.show()

    d=range(0,2)
    p=q=range(0,2)

    pdq=list(itertools.product(p,d,q))

    #递归确定pdq，选择AIC最小的
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
      
    import warnings
    warnings.filterwarnings("ignore") # specify to ignore warning messages
    tab = 1000000
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                model = sm.tsa.statespace.SARIMAX(data, order=param, seasonal_order=param_seasonal, enforce_stationarity=False, enforce_invertibility=False)
                results = model.fit()
                if results.aic<tab:
                    tab = results.aic
                    a = param
                    b = param_seasonal
                #print('ARIMA{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    print('ARIMA{}x{} - AIC:{}'.format(a, b, tab))
    model = sm.tsa.statespace.SARIMAX(data, order=(param), seasonal_order=(param_seasonal), enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit()
    print(results.summary().tables[1])

    results.plot_diagnostics(figsize=(12, 12))
    plt.show()

    #2000年开始预测测试
    pred = results.get_prediction(start=pd.to_datetime('2000-01-01'), dynamic=False)
    pred_ci = pred.conf_int()

    ax = data['1980':].plot(label='Observed',figsize=(12, 6))
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)
    
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Temp')
    plt.legend()
 
    plt.show()
    
    data_forecasted = pred.predicted_mean
    data_truth = data['2000-01-01':]

    # Compute the mean square error
    mse = ((data_forecasted - data_truth) ** 2).mean()
    print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

    # 未来7个月
    pred_uc = results.get_forecast(steps=7)
 
    # 区间
    pred_ci = pred_uc.conf_int()
    
    ax = data.plot(label='Observed', figsize=(50, 6))

    #具体值
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Temp')
 
    plt.legend()
    plt.show()


    print(pred_ci)#区间值
    print(pred_uc.predicted_mean)#具体值

    data1 = pd.DataFrame({'DATE':pred_uc.predicted_mean,'MAXT':pred_ci.iloc[:, 1],'MINT':pred_ci.iloc[:, 0]})
    data1.to_csv("D:/Forecast/"+station+".csv")
Sarima("ZhengZhou")