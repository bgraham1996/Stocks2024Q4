import pandas as pd
import yfinance as yf


#this function will download the stock data from yahoo finance for a given ticker and date range
def stock_request(ticker, start_data, end_data):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_data, end=end_data)
    stock_data.reset_index(inplace=True)
    if 'Dividends' in stock_data.columns:
        stock_data = stock_data.drop(columns=['Dividends'])
    if 'Stock Splits' in stock_data.columns:
        stock_data = stock_data.drop(columns=['Stock Splits'])
    stock_data['Ticker'] = ticker
    
    return stock_data


# this function will calculate the average price of the stock
def raw_data_process1(data):
    data['avg_price'] = (data['High'] + data['Low'] + data['Close']) / 3

    return data