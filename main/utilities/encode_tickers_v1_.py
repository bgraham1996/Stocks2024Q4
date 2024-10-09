import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_tickers(data):
    enc = OneHotEncoder()
    enc.fit(data[['Ticker']])
    encoded = enc.transform(data[['Ticker']]).toarray()
    encoded = pd.DataFrame(encoded, columns=enc.get_feature_names(['Ticker']))
    data = pd.concat([data, encoded], axis=1)
    data.drop(columns=['Ticker'], inplace=True)
    return data