# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:07:21 2020

@author: 94763
"""

#
# 博文参考：https://www.rs-online.com/designspark/lstm-1-cn
# 源码参考：https://github.com/danrustia11/WeatherLSTM
# LSTM weather prediction demo
# Written by: Dan R 2020
#


#
# Core Keras libraries
#
from numpy import array
from sklearn.metrics import r2_score # 拟合优度
from sklearn.metrics import mean_squared_error  # 均方差
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf  # 随机数生成器，结果可重现
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM  # LSTM
from keras.layers import Bidirectional  # 双向

#
# For data conditioning
#
from scipy.ndimage import gaussian_filter1d  # 数据调节
from scipy.signal import medfilt

#
# Make results reproducible
#
from numpy.random import seed
seed(1)

tf.random.set_seed(1)
#
# Other essential libraries
#

# Make our plot a bit formal
font = {'family': 'Arial',
        'weight': 'normal',
        'size': 10}
plt.rc('font', **font)


#
# Set input number of timestamps and training days
#
n_timestamp = 10  # 时间戳
train_days = 1500  # number of days to train from 开始的天数
testing_days = 500  # number of days to be predicted 可以预测的天数
n_epochs = 25  # 训练轮数
filter_on = 1  # 激活数据过滤器


#
# Select model type 选择型号类型
# 1: Single cell 单格
# 2: Stacked 堆叠
# 3: Bidirectional 双向
#
model_type = 2

#-----------------------------------------
# 数据集
#-----------------------------------------
# 台湾环境保护局提供的台湾宜兰县的每日环境温度
url = "D:/weather/result/BeiJing.csv"
dataset = pd.read_csv(url)
if filter_on == 1:  # 数据集过滤
    dataset['tavg'] = medfilt(dataset['tavg'], 3)  # 中值过滤
    dataset['tavg'] = gaussian_filter1d(
        dataset['tavg'], 1.2)  # 高斯过滤


#
# Set number of training and testing data 设置训练和测试数据集
#
train_set = dataset[0:train_days].reset_index(drop=True)
test_set = dataset[train_days: train_days+testing_days].reset_index(drop=True)
training_set = train_set.iloc[:, 1:2].values
testing_set = test_set.iloc[:, 1:2].values
#-----------------------------------------
# 数据集完
#-----------------------------------------


#
# Normalize data first
#
sc = MinMaxScaler(feature_range=(0, 1))  # 将数据标准化，范围是0到1
training_set_scaled = sc.fit_transform(training_set)
testing_set_scaled = sc.fit_transform(testing_set)

#
# Split data into n_timestamp
#
def data_split(sequence, n_timestamp):
    X = []
    y = []
    for i in range(len(sequence)):
        end_ix = i + n_timestamp
        if end_ix > len(sequence)-1:
            break
        # i to end_ix as input
        # end_ix as target output
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


X_train, y_train = data_split(training_set_scaled, n_timestamp)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test, y_test = data_split(testing_set_scaled, n_timestamp)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)


# 使用Keras建构LSTM模型
if model_type == 1:
    # Single cell LSTM
    model = Sequential()
    model.add(LSTM(units=50, activation='relu',
                   input_shape=(X_train.shape[1], 1)))
    model.add(Dense(units=1))
if model_type == 2:
    # Stacked LSTM
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True,
                   input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
if model_type == 3:
    # Bidirectional LSTM
    model = Sequential()
    model.add(Bidirectional(LSTM(50, activation='relu'),
                            input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))


#
# Start training 模型训练，batch_size越大越精准，训练消耗越大
#
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_train, y_train, epochs=n_epochs, batch_size=32)
loss = history.history['loss']
epochs = range(len(loss))


#
# Get predicted data 测试集预测
#
y_predicted = model.predict(X_test)

#
# 'De-normalize' the data 正规化将数据还原
#
y_predicted_descaled = sc.inverse_transform(y_predicted)
y_train_descaled = sc.inverse_transform(y_train)
y_test_descaled = sc.inverse_transform(y_test)
y_pred = y_predicted.ravel()
y_pred = [round(yx, 2) for yx in y_pred]
y_tested = y_test.ravel()


#
# Show results 显示预测结果，包括原始数据、n个预测天数和前75天
#
plt.figure(figsize=(8, 7))

plt.subplot(3, 1, 1)
plt.plot(dataset['tavg'], color='black',
         linewidth=1, label='True value')
plt.ylabel("tavg")
plt.xlabel("Day")
plt.title("All data")


plt.subplot(3, 2, 3)
plt.plot(y_test_descaled, color='black', linewidth=1, label='True value')
plt.plot(y_predicted_descaled, color='red',  linewidth=1, label='Predicted')
plt.legend(frameon=False)
plt.ylabel("tavg")
plt.xlabel("Day")
plt.title("Predicted data (n days)")

plt.subplot(3, 2, 4)
plt.plot(y_test_descaled[0:7], color='black', linewidth=1, label='True value')
plt.plot(y_predicted_descaled[0:7], color='red', label='Predicted')
plt.legend(frameon=False)
plt.ylabel("tavg")
plt.xlabel("Day")
plt.title("Predicted data (first 75 days)")
print(y_predicted_descaled[0:7])

plt.subplot(3, 3, 7)
plt.plot(epochs, loss, color='black')
plt.ylabel("Loss (MSE)")
plt.xlabel("Epoch")
plt.title("Training curve")

plt.subplot(3, 3, 8)
plt.plot(y_test_descaled-y_predicted_descaled, color='black')
plt.ylabel("Residual")
plt.xlabel("Day")
plt.title("Residual plot")

plt.subplot(3, 3, 9)
plt.scatter(y_predicted_descaled, y_test_descaled, s=2, color='black')
plt.ylabel("Y true")
plt.xlabel("Y predicted")
plt.title("Scatter plot")

plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()


mse = mean_squared_error(y_test_descaled, y_predicted_descaled) # 均方误差
r2 = r2_score(y_test_descaled, y_predicted_descaled) # 决定系数（拟合优度）接近1越好
print("mse=" + str(round(mse, 2)))
print("r2=" + str(round(r2, 2)))