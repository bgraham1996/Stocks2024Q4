import main as m
# need to update this to only import the necessary functions
import pandas as pd
import numpy as np

def RF_pipeline1 (start_date, end_date, irl_data_offset=5, 
                  periods = [5,10,15,20,25,30,40,50,60,70,80,90,100],
                  tickers = ['PFE'],
                  buy_thresholds = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
                  RF_option = 'basic', # basic = no warm start, warm_start = warm start
                  TSS_q = True,
                  TSS_s = 10,
                  debug = False):
    """
    list of actions:
    - download data
    - process data
    - split data
    - train model for each period
    - ideally we should have a different model for each buy threshold in each period
    - so we need to split the data for each buy threshold first then train a model for each period
    - we need to store the models in a dictionary
    - we then need to fit the model to the irl_test data to generate real world predictions
    
    """
    
    # start by converting the start and end dates to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    offset_date = end_date - pd.DateOffset(days=irl_data_offset)
    
        # determine if the RF_option is valid
    if RF_option == 'basic':
        RF_option = False
    elif RF_option == 'warm_start':
        RF_option = True
    else:
        raise ValueError('RF_option must be either "basic" or "warm_start"')
    
    #create an entry in a dictory for each buy threshold and its model
    models = {} # for storing models
    datasets = {} # for storing 
    
    #download the data and process it for each buy threshold
    for t in buy_thresholds:
        data1 = m.ticker_iter(tickers, start_date, offset_date, t, debug=debug)
        threshold = str(t).replace('.','_')
        datasets[threshold] = data1
        
        
    
    #split the data in test and train
    train, test = m.build_data_split(data, irl_data_offset)
    train = m.encode_tickers(train)
    
    #encode the tickers
    test = m.encode_tickers(test)
    
    
    # need to convert the periods to strings
    periods = [str(p) + '_return' for p in periods]

    for t in buy_thresholds:
        data = m.ticker_iter(tickers, start_date, end_date, t, periods=periods, debug=debug)
        forrest,  = m.period_iterator(train, periods, debug, RF_option)
        models[t] = models_s
        
        
        