import pandas as pd
import module as m

# need to update this function to take the threshold row from the matrix as an argument



def returns_encoder(data, periods =  
            [5,10,15,20,25,30,40,50,60,70,80,90,100],
            threshold = [0.0, 0.1, 0.0]):
    for period in periods:
        p = str(period)
        p_name = p + '_return'
        data[p_name] = data['avg_price'].shift(-period)
        data[p_name] = (data[p_name] - data['avg_price']) / data['avg_price']
        data[p_name] = data[p_name].apply(lambda x: column_encoder(x, threshold))

    return data

def column_encoder(column, thresholds = [0.0, 0.1, 0.0]):
    # lets handle lower bounds logic first
    if thresholds[0] == 'lower_bound':
        if column < thresholds[1]:
            return 1
        else:
            return 0
    # now lets handle upper bounds logic
    elif thresholds[1] == 'upper_bound':
        if column >= thresholds[2]:
            return 1
        else:
            return 0
    # now lets handle the rest of the logic
    elif column >= thresholds[0] and column < thresholds[1]:
        return 1
    else:
        return 0