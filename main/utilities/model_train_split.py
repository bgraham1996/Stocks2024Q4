import pandas as pd
import datetime as dt

# a function to seperate training and testing data from data
# to be used for live predictions
def build_data_split(data, train_start, train_end, test_start, test_end):
    train_data = data[(data['Date'] >= train_start) & (data['Date'] <= train_end)]
    test_data = data[(data['Date'] >= test_start) & (data['Date'] <= test_end)]
    
    return train_data, test_data