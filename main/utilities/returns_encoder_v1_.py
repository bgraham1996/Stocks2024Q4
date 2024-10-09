import pandas as pd

def returns_encoder(data, periods =  
            [5,10,15,20,25,30,40,50,60],
            threshold = 0.03):
    for period in periods:
        p = str(period)
        p_name = p + '_return'
        data[p_name] = data['avg_price'].shift(-period)
        data[p_name] = (data[p_name] - data['avg_price']) / data['avg_price']
        data[p_name] = data[p_name].apply(lambda x: 1 if x >= threshold else 0)

    return data