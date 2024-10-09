import pandas as pd
import main as m

def ticker_iter(ticker_list, start_date, end_date, buy_threshold):
    tickers = ticker_list
    start_date = start_date
    end_date = end_date
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits', 'Ticker', 'avg_price', '5','10','15','20','25','30','40','50','60', 'RSI_Signal', 'SMA_Signal', 'EMA_Signal', 'MACD_Signal', 'Bollinger_Signal', 'StochO_Signal', 'WillR_Signal', 'PSAR_Signal']
    master_returns = pd.DataFrame(columns=columns)
    
    for ticker in tickers:
        dh = m.stock_request(ticker, start_date, end_date)
        dh = m.raw_data_process1(dh)
        return_periods = m.returns(dh)
        pd.merge(dh, return_periods, left_index=True, right_index=True)
        # print(dh.head())
        
        # up to here it works fine
        # now I need to add the signals to the dataframe
        print(ticker)
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
        print('Data Downloaded and Processed')
        
    master_returns = m.returns_encoder(master_returns, threshold=buy_threshold)
    master_returns['year'] = pd.DataFrame(master_returns['Date']).reset_index()['Date'].dt.year
    master_returns['month'] = pd.DataFrame(master_returns['Date']).reset_index()['Date'].dt.month
    master_returns['quarter'] = pd.DataFrame(master_returns['Date']).reset_index()['Date'].dt.quarter

    
    
    return master_returns