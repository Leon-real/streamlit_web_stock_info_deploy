import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import FinanceDataReader as fdr

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from plotly import graph_objects as go

import tensorflow as tf
from keras.models import load_model
from keras.layers import Dense,Dropout,LSTM
from keras.models import Sequential

import streamlit as st


def get_data(code):
    df = fdr.DataReader(code)
    return df

# 차트 보여주기
def show_chart(code):
    df = get_data(code)
    df['ma100'] = df['Close'].rolling(100).mean() # 100일 이평선
    df['ma200'] = df['Close'].rolling(200).mean() # 200일 이평선

    df = df.dropna()
    df = df[-220:]
    fig = plt.figure(figsize=(12,6)) # 그래프 사이즈 설정

    plt.plot(df['ma100'], 'r', label='MA100') # 100일 이평선 빨간색으로 그리기
    plt.plot(df['ma200'], 'g', label='MA200') # 200일 이평선 녹색으로 그리기
    plt.plot(df['Close'], label='Close') # 종가 가격 그래프 그리기
    plt.legend()
    
    return fig
def show_chart_ver_2(code):
    df = get_data(code)
    df['ma100'] = df['Close'].rolling(100).mean() # 100일 이평선
    df['ma200'] = df['Close'].rolling(200).mean() # 200일 이평선
    
    df = df.dropna()
    df = df.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='stock_open'))
    fig.layout.update(title_text='Data', xaxis_rangeslider_visible=True)
    
    return fig

# 모델 생성하기
def several_model(code):
    df = get_data(code)
    # x, y 나누기
    target = 'target'
    x= df.drop(target, axis=1)
    y= df.loc[:, target]
    
    # train, test 나누기
    x_train = x[:int(len(x)*0.7)]
    x_test = x[int(len(x)*0.7):]

    y_train = y[:int(len(y)*0.7)]
    y_test = y[int(len(y)*0.7):]

    # 모델 생성
    # 1.세션 클리어
    tf.keras.backend.clear_session() 

    # 2. 모델 설정
    model = Sequential()
    model.add(LSTM(units=50,
                activation='relu',
                return_sequences=True,
                input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=60,
                activation='relu',
                return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(units=80,
                activation='relu',
                return_sequences=True))
    model.add(Dropout(0.4))

    model.add(LSTM(units=120,
                activation='relu',
                return_sequences=True,))
    model.add(Dropout(0.5))

    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.summary()
    
    model.fit(x_train, y_train, epochs=50)
    
    df['predict_price']=model.predict(x_test)
    fig = plt.figure(figsize=(12,6)) # 그래프 사이즈 설정
    plt.plot(df['Close'], label='Close') # 종가 가격 그래프 그리기
    plt.legend()
    
    return model