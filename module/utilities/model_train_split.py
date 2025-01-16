import pandas as pd
import datetime as dt

# a function to seperate training and testing data from data
# to be used for live predictions
def build_data_split(data, offset):
    end_data = data['Date'].max()
    train_end = end_data - dt.timedelta(days=offset)
    train_data = data[data['Date'] <= train_end]
    test_data = data[(data['Date'] > train_end)]
    
    return train_data, test_data