import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import TimeSeriesSplit
import time
import matplotlib.pyplot as plt
import seaborn as sns



def basic_rf(data, target='60_return', features = ['RSI_Signal', 'SMA_Signal', 'EMA_Signal', 'MACD_Signal', 'Bollinger_Signal', 'StochO_Signal', 'WillR_Signal', 'PSAR_Signal', 'year', 'month', 'quarter'], debug=True):
    preds = [] # for collection of predictions
 
    tss = TimeSeriesSplit(n_splits=10)
    fold = 0
    data.index = pd.to_datetime(data.index)
    feature_importances = []

    for train_idx, val_idx in tss.split(data):
        train = data.iloc[train_idx]
        val = data.iloc[val_idx]
        fold += 1

        # we get the target column from the target variable in the params, and the features from the features variable in the params
        # note that the features will be the same for each fold
        # note that for different periods in the input dataframe, only one target column will be used
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

        if debug == True:
            plt.figure(figsize=(20, 10))
            plt.plot(out.index, out['target'], label='target', c='green', alpha=0.5)
            plt.plot(out.index, out['pred'], label='pred', c='red', alpha=0.3)
            plt.plot
            plt.legend()
            plt.show()
            print("--------------------")

        preds.append(y_pred)
    return forrest, feature_importances, preds


def period_iterator(data, periods = [
    '5_return', '10_return', '15_return', '20_return', '25_return', '30_return', '40_return', '50_return', '60_return'], debug=True):
    models_dict = {}
    preds_dict = {}
    fi_dict = {}
    
    for period in periods:
        print('===========================================')
        print(f'Running for period: {period}')
        model, fi, preds = basic_rf(data, target=period, debug=debug)
        key = period
        models_dict[key] = model
        fi_dict[key] = fi
        preds_dict[key] = preds
    
    return models_dict, fi_dict, preds_dict
