
import pandas_ta as ta
import pandas as pd
import numpy as np
import datetime

# these functions are used to calculate the indicators for the stock data

# create a df for the indicators
def reset_dfs():
    indicator_columns = ['date', 'ticker', 'value', 'indicatorID', 'parameters']
    dfr = pd.DataFrame(columns=indicator_columns)
    return dfr


# gets the moving average of the stock
def sma(search_df, return_df, length):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    return_df['value'] = search_df['avg_price'].rolling(window=length).mean()
    return_df['indicatorID'] = 'sma'
    return_df['parameters'] = 'length=' + str(length)
    
    return return_df

# gets the exponential moving average of the stock
def ema(search_df, return_df, length):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    return_df['value'] = search_df['avg_price'].ewm(span=length, adjust=False).mean()
    return_df['indicatorID'] = 'ema'
    return_df['parameters'] = 'length=' + str(length)
    
    return return_df

# gets the relative strength index of the stock
def rsi(search_df, return_df, length):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    return_df['value'] = ta.rsi(search_df['avg_price'], length=length)
    return_df['indicatorID'] = 'rsi'
    return_df['parameters'] = 'length=' + str(length)
    
    return return_df


def macd(search_df, return_df, params = 
         {"windows" : 
          {"slow": 26, "fast": 12, "signal": 9},
          "return_value" : 2
          }):
    params = params
    slow = params['windows']['slow']
    fast = params['windows']['fast']
    singal = params['windows']['signal']
    return_value = params['return_value']
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    macd_data = ta.macd(search_df['Close'], fast=fast, slow=slow, signal=singal)
    print(type(macd_data))
    macd_data = macd_data.iloc[:, return_value]
    
    return_df['value'] = macd_data
    return_df['indicatorID'] = 'macd'
    return_df['parameters'] = 'length=' + str(params)
    
    return return_df

def bollinger(search_df, return_df, params = {
    "windows" : {
        "length" : 20,
        "std" : 2},
    "return_value" : 4
}):
    params = params
    length = params['windows']['length']
    std = params['windows']['std']
    return_value = params['return_value']
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']

    bands = ta.bbands(search_df['Close'], length=length, std=std)
    return_df['value'] = bands.iloc[:, return_value]

    return_df['indicatorID'] = 'bollinger'
    return_df['parameters'] = str(params)
    
    return return_df

def atr(search_df, return_df, length):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    return_df['value'] = ta.atr(search_df['High'], search_df['Low'], search_df['Close'], length=length)
    return_df['indicatorID'] = 'atr'
    return_df['parameters'] = 'length=' + str(length)
    
    return return_df

def stocho(search_df, return_df, params = {
    "length" : 14,
    "return_value" : 0
}):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']

    result =  ta.stoch(search_df['High'], search_df['Low'], search_df['Close'], length=params['length'])
    return_df['value'] = result.iloc[:, (params['return_value'])]
    return_df['indicatorID'] = 'stocho'
    return_df['parameters'] = str(params)
    
    return return_df

def willR(search_df, return_df, params):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    return_df['value'] = ta.willr(search_df['High'], search_df['Low'], search_df['Close'], length=params['length'])
    return_df['indicatorID'] = 'willR'
    return_df['parameters'] = str(params)
    
    return return_df

def psar(search_df, return_df, acceleration, maximum):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']

    result = ta.psar(search_df['High'], search_df['Low'], acceleration=acceleration, maximum=maximum)

    return_df['value'] = result.iloc[:, 0]
    return_df['indicatorID'] = 'psar'
    return_df['parameters'] = 'acceleration=' + str(acceleration) + ', maximum=' + str(maximum)
    
    return return_df



def obv(search_df, return_df):
    return_df['date'] = search_df['Date']
    return_df['ticker'] = search_df['Ticker']
    return_df['value'] = ta.obv(search_df['Close'], search_df['Volume'])
    return_df['indicatorID'] = 'obv'
    return_df['parameters'] = 'none'
    
    return return_df





