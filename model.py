from env import host, user, password
   
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from math import sqrt
import seaborn as sns

from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression 
from sklearn.preprocessing import MinMaxScaler

import wrangle
import warnings
warnings.filterwarnings('ignore')

## Most of these functions were not scripted yet and included in the presentation notebook
### will create functions soon for a cleaner presentation (short of time)

########
# def xy_train_val_test():
#     #get data from wrangle
#     df = wrangle.get_zillow_data()
#     #prepare data from wrangle
#     df = wrangle.prepare(df)
#     #splits data from wrangle   
#     train, validate, test = wrangle.split_data(df)
#     train, validate, test, = scale_zillow(train, validate, test)
#     scaled = ['bathroom_count_scaled', 'bedroom_count_scaled', 'square_feet_scaled']

#     X_train = train[scaled]
#     y_train = train.tax_value

#     X_validate = validate[scaled]
#     y_validate = validate.tax_value

#     X_test = test[scaled]
#     y_test = test.tax_value

#     return X_train, y_train, X_validate, y_validate, X_test, y_test


#######
def regression_errors(y, y_hat):
    #calculate residuals
    residuals = y - y_hat
    
    #residuals squared
    residuals_squared = residuals ** 2
    
    #sum of squared errors
    SSE = residuals_squared.sum()
    
    #explained sum of squares
    ESS = sum((y_hat - y.mean()) ** 2)
    
    #total sum of squares
    TSS = ESS + SSE
    
    #mean of squared errors
    MSE = SSE / len(y)
    
    #root of mean of squared errors
    RMSE = MSE ** (1/2)
    
    #gimme gimme
    print('Model Metrics')
    print('=============')
    return pd.Series({
        'SSE': SSE,
        'ESS': ESS,
        'TSS': TSS,
        'MSE': MSE,
        'RMSE': RMSE
    })

    ###################
#     def baseline():
#     xy_train_val_test(X_train, y_train, X_validate, y_validate, X_test, y_test)
    
#     #turning my y_train and y_validate to dataframes so we can append new columns
#     y_train = pd.DataFrame(y_train)
#     y_validate = pd.DataFrame(y_validate)

#     #tax_value mean
#     tax_value_pred_mean = y_train['tax_value'].mean()
#     y_train['tax_value_pred_mean'] = tax_value_pred_mean
#     y_validate['tax_value_pred_mean'] = tax_value_pred_mean

#     #tax_value_median
#     tax_value_pred_median = y_train['tax_value'].median()
#     y_train['tax_value_pred_median'] = tax_value_pred_median
#     y_validate['tax_value_pred_median'] = tax_value_pred_median

#     #RMSE of tax_value_pred_mean
#     rmse_train_mean = mean_squared_error(y_train.tax_value, y_train.tax_value_pred_mean)**(1/2)
#     rmse_validate_mean = mean_squared_error(y_validate.tax_value, y_validate.tax_value_pred_mean)**(1/2)

#     print('             BASELINE')
#     print('----------------------------------')
#     print("RMSE using Mean\nTrain/In-Sample: ", round(rmse_train_mean, 2), 
#           "\nValidate/Out-of-Sample: ", round(rmse_validate_mean, 2))
#     print('----------------------------------')

#     #RMSE of tax_value_pred_median
#     rmse_train_median = mean_squared_error(y_train.tax_value, y_train.tax_value_pred_median)**(1/2)
#     rmse_validate_median = mean_squared_error(y_validate.tax_value, y_validate.tax_value_pred_median)**(1/2)

#     print("RMSE using Median\nTrain/In-Sample: ", round(rmse_train_median, 2), 
#           "\nValidate/Out-of-Sample: ", round(rmse_validate_median, 2))
#     print('----------------------------------')
#     r2_baseline = r2_score(y_validate.tax_value, y_validate.tax_value_pred_mean)
#     print(f'The r^2 score for baseline is {r2_baseline}')
    
# #####