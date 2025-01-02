import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import TimeSeriesSplit
import time
import matplotlib.pyplot as plt
import seaborn as sns



def basic_rf(data, target='60_return', features=['RSI_Signal', 'SMA_Signal', 'EMA_Signal', 
             'MACD_Signal', 'Bollinger_Signal', 'StochO_Signal', 'WillR_Signal', 
             'PSAR_Signal', 'year', 'month', 'quarter'], debug=True, warm_start=True, tss_s=10):
    # Initialize collections
    preds = []  
    feature_importances = []
    
    # Initialize the Random Forest once before the loop if using warm_start
    if warm_start == True:
        forrest = RandomForestClassifier(n_estimators=50, random_state=42, warm_start=True)

    
    # Process ticker columns
    columns = data.columns
    for column in columns:
        if 'Ticker' in column:
            features.append(column)
    
    # Setup time series split
    tss = TimeSeriesSplit(n_splits=tss_s)
    fold = 0
    data.index = pd.to_datetime(data.index)
    
    # Iterate through folds
    for train_idx, val_idx in tss.split(data):
        train = data.iloc[train_idx]
        val = data.iloc[val_idx]
        fold += 1
        
        # Prepare features and target
        x_train = train[features]
        y_train = train[target]
        x_val = val[features]
        y_val = val[target]
        
        # Fit and predict
        if warm_start == False:
            forrest = RandomForestClassifier(n_estimators=100, random_state=42)
        forrest.fit(x_train, y_train)
        y_pred = forrest.predict(x_val)
        
        if warm_start == True:
            forrest.n_estimators += 10
        
        # Print metrics
        print("--------------------")
        print(f'Fold: {fold}')
        print(f'Accuracy: {forrest.score(x_val, y_val)}')
        print('confusion_matrix:')
        cf = pd.crosstab(y_val, y_pred)
        print(cf)
        
        # Calculate and print class-specific accuracies
        all_positives = cf[1].sum()
        positive_accuracy = cf[1][1] / all_positives if all_positives > 0 else 0
        print(f'Positive Accuracy: {positive_accuracy}')
        
        all_negatives = cf[0].sum()
        negative_accuracy = cf[0][0] / all_negatives if all_negatives > 0 else 0
        print(f'Negative Accuracy: {negative_accuracy}')
        
        # Store results
        feature_importances.append(forrest.feature_importances_)
        
        # Debug visualization
        if debug:
            out = pd.DataFrame()
            out['target'] = y_val
            out['pred'] = y_pred
            out['correct'] = out['target'] == out['pred']
            out = out.tail(300)
            #print(x_train.head(10))
            #print(x_train.tail(10))
            
            plt.figure(figsize=(20, 10))
            plt.plot(out.index, out['target'], label='target', c='green', alpha=0.5)
            plt.plot(out.index, out['pred'], label='pred', c='red', alpha=0.3)
            plt.legend()
            plt.show()
            print("--------------------")
        
        preds.append(y_pred)
    
    return forrest, feature_importances, preds


def period_iterator(data, periods = [
    '5', '10', '15', '20', '25', '30', '40', '50', '60', '70', '80', '90', '100'], 
                    debug=True, 
                    warm_start=True,
                    tss_s = 10):
    models_dict = {}
    preds_dict = {}
    fi_dict = {}
    
    for period in periods:
        period str(period) + '_return'
        print('===========================================')
        print(f'Running for period: {period}')
        model, fi, preds = basic_rf(data, target=period, debug=debug, warm_start=warm_start)
        key = period
        models_dict[key] = model
        fi_dict[key] = fi
        preds_dict[key] = preds
    
    return models_dict, fi_dict, preds_dict