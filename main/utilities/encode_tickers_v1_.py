import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_tickers(data):
    encoded = pd.get_dummies(data['Ticker'], prefix='Ticker')
    data = pd.concat([data, encoded], axis=1)
    data.drop(columns=['Ticker'], inplace=True)
    return data




""" def encode_tickers(data):
    enc = OneHotEncoder()
    enc.fit(data[['Ticker']])
    encoded = enc.transform(data[['Ticker']]).toarray()
    encoded = pd.DataFrame(encoded, columns=enc.get_feature_names_out(['Ticker']))
    data = pd.concat([data, encoded], axis=1)
    data.drop(columns=['Ticker'], inplace=True)
    return data """