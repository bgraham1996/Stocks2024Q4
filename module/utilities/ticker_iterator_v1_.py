import pandas as pd
import module as m

"""
The ticker_iterator_v1_.py file contains the following functions:

ticker_iter(ticker_list, start_date, end_date, buy_threshold, debug=False): 
This function iterates over a list of tickers and retrieves stock data for each
ticker within the specified date range. It calculates various technical indicators 
such as RSI, SMA, EMA, MACD, Bollinger Bands, Stochastic Oscillator, 
Williams %R, and Parabolic SAR. It then combines the data into a master 
dataframe and encodes the returns based on a specified threshold. 
The function returns the master dataframe with additional columns for 
signals and time-related information.

Inputs:

ticker_list (list): List of tickers to retrieve data for.
start_date (str): Start date of the data range in the format 'YYYY-MM-DD'.
end_date (str): End date of the data range in the format 'YYYY-MM-DD'.
buy_threshold (float): Threshold value for encoding the returns.
debug (bool, optional): Flag to enable debug mode. Defaults to False.

Output:

master_returns (DataFrame): Master dataframe containing the processed stock data with additional columns for signals, returns, and time-related information.
"""

def ticker_iter(ticker_list, start_date, end_date, buy_threshold, debug = False, periods = [5, 10, 15, 20, 25, 30, 40, 50, 60]):
    tickers = ticker_list
    start_date = start_date
    end_date = end_date
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits', 'Ticker', 'avg_price', '5','10','15','20','25','30','40','50','60', 'RSI_Signal', 'SMA_Signal', 'EMA_Signal', 'MACD_Signal', 'Bollinger_Signal', 'StochO_Signal', 'WillR_Signal', 'PSAR_Signal']
    master_returns = pd.DataFrame(columns=columns)
    
    # download the data, then calculate the returns and indicators
    for ticker in tickers:
        if debug == True:
            print(ticker)
        dh = m.stock_request(ticker, start_date, end_date)
        dh = m.raw_data_process1(dh)
        return_periods = m.returns(dh)
        pd.merge(dh, return_periods, left_index=True, right_index=True)
        # print(dh.head())
        
        # up to here it works fine
        # now I need to add the signals to the dataframe
        #print(ticker)
        dh_rsi, p = m.simple_rsi_buy_rule_v1(dh)
        #pd.merge(dh, dh_rsi, left_index=True, right_index=True)
        dh['RSI_Signal'] = dh_rsi['signal']
        
        dh_sma = m.sma_cross_over_signal(dh)
        dh['SMA_Signal'] = dh_sma['signal']
        
        dh_ema,p = m.simple_ema_cross_v1(dh)
        dh['EMA_Signal'] = dh_ema['signal']
        
        dh_macd, p = m.simple_macd_cross_v1(dh)
        dh['MACD_Signal'] = dh_macd['signal']
        
        dh_bollinger, p = m.simple_bollinger_cross_v1(dh)
        dh['Bollinger_Signal'] = dh_bollinger['signal']
        
        dh_stocho, p = m.simple_stocho_band_cross(dh)
        dh['StochO_Signal'] = dh_stocho['signal']
        
        dh_willR, p = m.willR_signal(dh)
        dh['WillR_Signal'] = dh_willR['signal']
        
        dh_psar, p = m.simple_psar_cross(dh)
        dh['PSAR_Signal'] = dh_psar['signal']
        
        
        master_returns = pd.concat([master_returns, dh])
        #print('Data Downloaded and Processed'))
    
    master_returns = m.returns_encoder(master_returns, threshold=buy_threshold, periods=periods)
    master_returns['year'] = pd.DataFrame(master_returns['Date']).reset_index()['Date'].dt.year
    master_returns['month'] = pd.DataFrame(master_returns['Date']).reset_index()['Date'].dt.month
    master_returns['quarter'] = pd.DataFrame(master_returns['Date']).reset_index()['Date'].dt.quarter

    
    
    return master_returns