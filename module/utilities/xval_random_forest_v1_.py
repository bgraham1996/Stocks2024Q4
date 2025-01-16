def xval_random_forest_v1(data, time_split_params, forest_params):
    X = data.drop(columns=['Date', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits', 'avg_price', '5','10','15','20','25','30','40','50','60'])
    y = data['avg_price']
    tscv = TimeSeriesSplit(**time_split_params)
    feature_importances = []
    models = []
    fold = 0
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        rf = RandomForestClassifier(**forest_params)
        rf.fit(X_train, y_train)
        print(rf.score(X_test, y_test))
        feature_importances.append(rf.feature_importances_)
        models.append(rf)
        print(rf.predict(X_test))
        print(y_test)
        
        
        fold += 1
    
    return rf