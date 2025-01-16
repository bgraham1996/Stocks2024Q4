import pandas as pd

# this function calculates the returns for the given data
# returns are calcluated as decimal values, not percentages

def returns(data, periods =  
            [5,10,15,20,25,30,40,50,60,70,80]):
    for period in periods:
        p = str(period) + '_return'
        data[p] = data['avg_price'].shift(-period)
        data[p] = (data[p] - data['avg_price']) / data['avg_price']

    return data