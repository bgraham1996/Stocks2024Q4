



import pandas as pd
import numpy as np
import datetime as dt
import main as m


# a function for creating a signal for when a stock crosses dual limits, eg rsi
def dual_limit_signal_manager(dff, params):
    p = params
    data = dff

    limits = False
    limit_pattern = 0
    default_limit_pattern = {'0': {'upper': '1', 'lower': '-1'}, '1': {'upper': '-1', 'lower': '1'}}
    
    if 'limits' in p:
        if 'upper' and 'lower' in p['limits']:
            upper = p['limits']['upper']
            lower = p['limits']['lower']
            limits = True
            limit_pattern = params['limit_pattern']
        
        if limits == True:
            data['signal'] = data['value'].apply(lambda x: int(default_limit_pattern[str(limit_pattern)]['upper']) if x > upper else (int(default_limit_pattern[str(limit_pattern)]['lower']) if x < lower else 0))
    
    return data
    
    
    
def simple_rsi_buy_rule_v1(
        ta_df, 
        rsi_params = {
            "limits" : {
                "upper" : 70,
                "lower" : 30
            },
            "limit_pattern" : 1
        }
    ):
    data = ta_df

    data = m.rsi(data, m.reset_dfs(), 14)

    data['signal'] = 0
    data = dual_limit_signal_manager(data, rsi_params)

    return data, rsi_params

# sma cross over signal

def sma_cross_over_signal(df, params = {
    "lengths" : {
        "short" : 20,
        "long" : 50
    }
}):
    df = df
    params = params
    short = m.sma(df, m.reset_dfs(), params['lengths']['short'])
    long = m.sma(df, m.reset_dfs(), params['lengths']['long'])
    short['lag'] = 0
    short['lag'] = long['value']
    short['i1'] = short['value'] - short['lag']
    short['i2'] = short['i1'].shift(1)
    short['value'] = short['i1']
    short['signal'] = 0
    short['signal'] = np.where((short['i1'] > 0) & (short['i2'] < 0), 1, short['signal'])
    short['signal'] = np.where((short['i1'] < 0) & (short['i2'] > 0), -1, short['signal'])
    short.drop(columns=['lag', 'i1', 'i2'], inplace=True)

    return short

# setting up the ema rule

def simple_ema_cross_v1(df,
                        params = {
                            "periods" : {
                                "short" : 20,
                                "long" : 50
                            }
                            }):
    ema_df = m.reset_dfs()
    short = m.ema(df, ema_df, params['periods']['short'])
   
    ema_df = m.reset_dfs()
    long = m.ema(df, ema_df, params['periods']['long'])
    

    short = pd.merge(short, long, on='date', how='outer')
    

    short['c_signal'] = 0
    short['c_signal'] = np.where(short['value_x'] > short['value_y'], 1, short['c_signal'])
    short['c_signal'] = np.where(short['value_x'] < short['value_y'], -1, short['c_signal'])
    short['lag'] = short['c_signal'].shift(1)
    short['signal'] = 0
    short['signal'] = np.where((short['c_signal'] == 1 ) & (short['lag'] < 1), 1, short['signal'])
    short['signal'] = np.where((short['c_signal'] == -1 ) & (short['lag'] > -1), -1, short['signal'])

    short['value'] = short['value_x'] - short['value_y']
    short.drop(columns=['c_signal', 'lag'], inplace=True)
    short.drop(columns=['value_x', 'value_y'], inplace=True)
    short.drop(columns=['ticker_y'], inplace=True)
    short.rename(columns={'ticker_x': 'ticker'}, inplace=True)
    short['parameters'] = short['parameters_x'] + ', ' + short['parameters_y']
    short.drop(columns=['parameters_x', 'parameters_y'], inplace=True)

    return short, params



def simple_macd_cross_v1(df, params = {
    "windows" : {
        "slow" : 26,
        "fast" : 12,
        "signal" : 9
    },
    "return_value" : 2
}):
    df = df
    params = params

    result = m.macd(df, m.reset_dfs(), params)
    result['c_signal'] = 0
    result['c_signal'] = np.where(result['value'] > 0, 1, result['c_signal'])
    result['c_signal'] = np.where(result['value'] < 0, -1, result['c_signal'])
    result['lag'] = result['c_signal'].shift(1)
    result['signal'] = 0
    result['signal'] = np.where((result['c_signal'] == 1 ) & (result['lag'] < 1), 1, result['signal'])
    result['signal'] = np.where((result['c_signal'] == -1 ) & (result['lag'] > -1), -1, result['signal'])
    
    result.drop(columns=['c_signal', 'lag'], inplace=True)

    return result, params
    
    
def simple_bollinger_cross_v1(df, params = {
    "windows" : {
        "length" : 20,
        "std" : 2
    },
    "return_value" : 4,
    "limits" : {
        "upper" : 1,
        "lower" : -1
    }
}):
    params = params
    result = m.bollinger(df, m.reset_dfs(), params)
    result['signal'] = 0

    result['signal'] = np.where(result['value'] > 1, 1, result['signal'])
    result['signal'] = np.where(result['value'] < -1, -1, result['signal'])
    

    return result, params


def simple_stocho_band_cross(df, params = {
    "length" : 14,
    "return_value" : 0,
    "limits" : {
        "upper" : 80,
        "lower" : 20
    }
}):
    params = params
    result = m.stocho(df, m.reset_dfs(), params)
    result['signal'] = 0

    result['signal'] = np.where(result['value'] > params['limits']['upper'], 1, result['signal'])
    result['signal'] = np.where(result['value'] < params['limits']['lower'], -1, result['signal'])
    

    return result, params

def willR_signal(df, params = {
    "length" : 14,
    "limits" : {
        "upper" : -20,
        "lower" : -80
    }
}):
    params = params
    result = m.willR(df, m.reset_dfs(), params)
    result['signal'] = 0

    result['signal'] = np.where(result['value'] > params['limits']['upper'], 1, result['signal'])
    result['signal'] = np.where(result['value'] < params['limits']['lower'], -1, result['signal'])
    

    return result, params


def simple_psar_cross(df, params = {
    "acceleration" : 0.02,
    "maximum" : 0.2
}):
    params = params
    result = m.psar(df, m.reset_dfs(), params['acceleration'], params['maximum'])
    result['signal'] = 0

    result['signal'] = np.where(result['value'] > df['Close'], 1, result['signal'])
    result['signal'] = np.where(result['value'] < df['Close'], -1, result['signal'])
    

    return result, params