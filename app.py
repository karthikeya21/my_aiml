import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

start='2012-01-01'
end='2022-12-31'

st.title('Stock Trend Prediction')
user_input = st.text_input('Enter stock Ticker','NFLX')
df = yf.download(user_input, start='2012-01-01', end='2022-12-31')

st.subheader('Data from 2012-2022')
st.write(df.describe())

#statistical visualizations
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize=(10,5))
plt.plot(df.Close,'k')
plt.xlabel('Time')
plt.ylabel('Price')
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(10,5))
plt.plot(ma100,'c',label='100MA')
plt.plot(df.Close,'m',label='Original price')
plt.xlabel('Time')
plt.ylabel('Price')
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart with 100MA and 200MA ')
ma200 = df.Close.rolling(200).mean()
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(10,5))
plt.plot(ma200,'g',label='200MA')
plt.plot(ma100,'r',label='100MA')
plt.plot(df.Close,'b',label='Original price')
plt.xlabel('Time')
plt.ylabel('Price')
st.pyplot(fig)

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
print(data_training.shape)
print(data_testing.shape)


scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)

#load my model
model = load_model('keras_model.h5')
#testing part
past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing,ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test,y_test=[],[]
for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])
x_test,y_test = np.array(x_test),np.array(y_test)

y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

#final predictions
st.subheader('Predictions vs Original')
fig2 = plt.figure(figsize=(10,5))
plt.plot(y_test,'c',label='Original price')
plt.plot(y_predicted,'y',label='Predicted price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
