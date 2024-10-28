import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import TimeSeriesSplit
import time
import matplotlib.pyplot as plt
import seaborn as sns



def wam_start_rf(data, target='60_return', features = ['RSI_Signal', 'SMA_Signal', 'EMA_Signal', 'MACD_Signal', 'Bollinger_Signal', 'StochO_Signal', 'WillR_Signal', 'PSAR_Signal', 'year', 'month', 'quarter'], debug=True):
    preds = [] # for collection of predictions
 
 
    # need a way to use the ticket columns as features
    columns = data.columns
    for column in columns:
        if 'Ticker' in column:
            features.append(column)
 
    tss = TimeSeriesSplit(n_splits=10) # splits the data into 10 folds
    fold = 0 # fold counter
    data.index = pd.to_datetime(data.index) # make sure the index is a datetime object
    feature_importances = [] # for collection of feature importances

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
        
        cf = pd.crosstab(y_val, y_pred)
        all_positives = cf[1].sum()
        positive_accuracy = cf[1][1] / all_positives
        print(f'Positive Accuracy: {positive_accuracy}')
        
        all_negatives = cf[0].sum()
        negative_accuracy = cf[0][0] / all_negatives
        print(f'Negative Accuracy: {negative_accuracy}')

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