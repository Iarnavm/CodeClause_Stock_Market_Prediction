# -*- coding: utf-8 -*-
"""Stock.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qwTpJhXRnax1h1VXk6XjNw2ngjOs2hfx

**`IMPORTING ALL THE REQUIRED LIBRARIES`**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

"""**`Using API of Kaggle, we will get the dataset`**"""

!pip install kaggle
from google.colab import files
files.upload() # Upload the Kaggle API token

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d rohanrao/nifty50-stock-market-data -p /content

"""**`Reading the dataset`**"""

df = pd.read_csv("/content/TATASTEEL.csv")

"""**`Preprocess the data`**"""

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1,1))

prediction_days = 60
X_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
    X_train.append(scaled_data[x-prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

X_train = np.array(X_train)
y_train = np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

"""**`LSTM MODEL`**"""

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=25, batch_size=32)

"""**`Prediction`**"""

test_start = '2020-01-01'
test_end = '2021-04-01'

test_df = df[(df['Date'] >= test_start) & (df['Date'] <= test_end)]
actual_prices = test_df['Close'].values

total_dataset = pd.concat((df['Close'], test_df['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_df) - prediction_days:].values
model_inputs = model_inputs.reshape(-1,1)
model_inputs = scaler.transform(model_inputs)

X_test = []
for x in range(prediction_days, len(model_inputs)):
    X_test.append(model_inputs[x-prediction_days:x, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

plt.plot(actual_prices, color='blue', label='Actual TataSteel Price')
plt.plot(predicted_prices, color='red', label='Predicted TataSteel Price')
plt.title('NSEI Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('TataSteel Stock Price')
plt.legend()
plt.show()