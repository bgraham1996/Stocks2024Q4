import pandas as pd
def threshold_matrix(threholds):
    
    length = len(threholds) - 1
    
    #creating the lower bounds of the matrix
    i = 0
    lower_bounds = []
    for t in threholds:

        print('i: ', i)

        if i == 0:
            bound = 'lower_bound'
        else:
            bound = t
        lower_bounds.append(bound)
        i += 1
    
    i = 0
    upper_bounds = []
    for t in threholds:

        print('i: ', i)

        if i == length:
            bound = 'upper_bound'
        else: 
            bound = threholds[i+1]
        upper_bounds.append(bound)
        i += 1
        
    matrix = pd.DataFrame(columns = ['lower_bound', 'upper_bound', 'thresholds'])
    matrix['lower_bound'] = lower_bounds
    matrix['upper_bound'] = upper_bounds
    matrix['thresholds'] = threholds       
    
    return matrix


    """
    this function creates a matrix of thresholds for the returns of the stock data
    
    It should create a datadfame with the following columns:
    lower_bound: the lower bound of the threshold
    upper_bound: the upper bound of the threshold
    thresholds: the threshold values
    
    an example of the output is:
    
    lower_bound | upper_bound | thresholds
    0.00        | 0.01        | 0.00
    0.01        | 0.02        | 0.01
    0.02        | upper_bound | 0.02
    lower_bound | 0.00        | -0.01    
    
    """
    
    # next task is top update the pipeline to include this funciton and enable
    # the downstream functions to use the matrix rows when interating through
    # also need to add the import statements