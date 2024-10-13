import pandas as pd
import numpy as np
import main as bg
import multi_ticker_iterator_v1 as iter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import TimeSeriesSplit
import time
import matplotlib.pyplot as plt
import seaborn as sns



def basic_rf(data, target='60_return', features = ['RSI_Signal', 'SMA_Signal', 'EMA_Signal', 'MACD_Signal', 'Bollinger_Signal', 'StochO_Signal', 'WillR_Signal', 'PSAR_Signal', 'year', 'month', 'quarter']):
    preds = []
    scores = []
    tss = TimeSeriesSplit(n_splits=10)
    fold = 0
    data.index = pd.to_datetime(data.index)
    feature_importances = []

    for train_idx, val_idx in tss.split(data):
        train = data.iloc[train_idx]
        val = data.iloc[val_idx]
        fold += 1

        x_train = train[features]
        y_train = train[target]

        x_val = val[features]
        y_val = val[target]

        forrest = RandomForestClassifier(n_estimators=100, random_state=42)
        forrest.fit(x_train, y_train)

        y_pred = forrest.predict(x_val)
        print("--------------------")
        print(f'Fold: {fold}')
        print(f'Accuracy: {forrest.score(x_val, y_val)}')
        print('confusion_matrix:')
        print(pd.crosstab(y_val, y_pred))

        feature_importances.append(forrest.feature_importances_)

        out = pd.DataFrame()
        out['target'] = y_val
        out['pred'] = y_pred
        out['correct'] = out['target'] == out['pred']
        out = out.tail(300)

        plt.plot(out.index, out['target'], label='target', c='green')
        plt.plot(out.index, out['pred'], label='pred', c='red')
        plt.plot
        plt.legend()
        plt.show()
        print("--------------------")
        preds.append(y_pred)
    return preds

