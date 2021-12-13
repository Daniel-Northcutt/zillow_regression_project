import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from env import host, user, password
from sklearn.model_selection import train_test_split
import sklearn.preprocessing

from scipy import stats
from math import sqrt
from statsmodels.formula.api import ols

from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
import sklearn.preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression 


import wrangle
#***********Franework for import to new functions***************

# train, validate, test = wrangle.wrangle_zillow()
# df = wrangle.get_zillow_data()
# df = wrangle.prepare(df)
# train, validate, test = wrangle.split_data()
# train, validate, test = wrangle.scale_zillow()
#####
def county_countplot():
    '''shows representation of county count of database'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    plt.figure(figsize=(12, 8))
    sns.countplot(data=df, x='county')
    plt.title('Database ')
    #plt.xticks([0, 1, 2], ['Orange: 6756', 'Ventura: 2159', 'LA: 16420'])
#####
def age_graph():
    '''shows home age distribution'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    ##
    plt.figure(figsize=(14, 6))
    age_graph = sns.histplot(data=df, x="age", discrete = True)
    age_graph.set(Title = "Property Age Distribution", xlabel = "Age of the Home", ylabel = "Number of Homes")

######
def county_tax_value():
    ''' shows representation of taxvaluation by county hue'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    plt.figure(figsize=(12, 6))
    sns.histplot(data = df, x='tax_value', hue='county', palette = 'twilight_shifted')
    plt.title('County Distribution by Tax Valuation')

###### Heatmap Correlation ####
def plot_train_heatmap():
    ''' Plots heatmap on split cleaned data - train dataset'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    #splits data from wrangle
    train, validate, test = wrangle.split_data(df)
    features = ['square_feet', 'bedroom_count', 'bathroom_count',  'age', 'tax_value']
 
    plt.figure(figsize=(16, 6))
    sns.heatmap(train[features].corr(), cmap="coolwarm", vmin=-1, vmax=1, annot=True, 
                           center=0, linewidths=4)
    plt.title('Zillow Correlation Heatmap of Trained Data', fontsize=18, pad=12)


####### bathroom_taxvalue_corr #######
def bathroom_taxvalue_corr():
    ''' Runs a correlation test between bathroom count and tax valuation,
    plots a box plot'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    #splits data from wrangle
    train, validate, test = wrangle.split_data(df)
    #State hypothesis: 
    null_hypothesis = "There is no correlation between the number of bathrooms and the tax value of a home"
    alt_hypothesis = "There is a correlation between the number of bathrooms and tax value of a home."
    #alpha
    α = .05
    # set x and y
    x = train.bathroom_count
    y= train.tax_value
    # run it
    corr, p = stats.pearsonr(x, y)
    print(f' The correlation between the number of bathrooms and the tax value is: {corr:.2f}')
    print(f' The P value between the number of bathrooms and tax value is: ', p)
    print(' ')
    if p < α:
        print(f"Reject null hypothesis:\n '{null_hypothesis}'")
        print('\n')
        print(f"We now move forward with our alternative hypothesis: '{alt_hypothesis}'")
        print('\n')
        if 0 < corr < .5:
            print("This is a weak positive correlation.")
        elif .5 < corr < 1:
            print("That is a strong positive correlation.")
        elif -.5 < corr < 0:
            print("This is a weak negative correlation.")
        elif -1 < corr < -.5:
            print("That is a strong negative correlation.")
    
    else : 
        print("Fail to reject the null hypothesis.")
    sns.boxplot(y='tax_value', x ='bathroom_count', data = train, palette='Set2')

    # BOOYAH!

####### bedroom_taxvalue_corr #######
def bedroom_taxvalue_corr():
    ''' Runs a correlation test between bedroom count and tax valuation,
    plots a box plot'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    #splits data from wrangle
    train, validate, test = wrangle.split_data(df)
    #State hypothesis: 
    null_hypothesis = "There is no correlation between the number of bedrooms and the tax value of a home"
    alt_hypothesis = "There is a correlation between the number of bedrooms and tax value of a home."
    #alpha
    α = .05
    # set x and y
    x = train.bedroom_count
    y= train.tax_value
    # run it
    corr2, p2 = stats.pearsonr(x, y)
    print(f' The correlation between the number of bedrooms and the tax value is: {corr2:.2f}')
    print(f' The P value between the number of bedrooms and tax value is:  {p2:.2f}')
    print(' ')
    if p2 < α:
        print(f"Reject null hypothesis:\n '{null_hypothesis}'")
        print('\n')
        print(f"We now move forward with our alternative hypothesis: '{alt_hypothesis}'")
        print('\n')
        if 0 < corr2 < .5:
            print("This is a weak positive correlation.")
        elif .5 < corr2 < 1:
            print("That is a strong positive correlation.")
        elif -.5 < corr2 < 0:
            print("This is a weak negative correlation.")
        elif -1 < corr2 < -.5:
            print("That is a strong negative correlation.")
    
    else : 
        print("Fail to reject the null hypothesis.")
    sns.boxplot(y='tax_value', x ='bedroom_count', data = train, palette='Set2')


####### squarefeet_taxvalue_corr #######

def squarefeet_taxvalue_corr():
    ''' Runs a correlation test between square feet and tax valuation,
    plots a box plot'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    #splits data from wrangle
    train, validate, test = wrangle.split_data(df)
    #State hypothesis: 
    null_hypothesis = "There is no correlation between the square feet and the tax value of a home"
    alt_hypothesis = "There is a correlation between the square feet and tax value of a home."
    #alpha
    α = .05
    # set x and y
    x = train.square_feet
    y= train.tax_value
    # run it
    corr, p = stats.pearsonr(x, y)
    print(f' The correlation between the square feet of a home and the tax value is: {corr:.2f}')
    print(f' The P value between the square feet of a home and tax value is:  {p:.2f}')
    print(' ')
    if p < α:
        print(f"Reject null hypothesis:\n '{null_hypothesis}'")
        print('\n')
        print(f"We now move forward with our alternative hypothesis: '{alt_hypothesis}'")
        print('\n')
        if 0 < corr < .5:
            print("This is a weak positive correlation.")
        elif .5 < corr < 1:
            print("That is a strong positive correlation.")
        elif -.5 < corr < 0:
            print("This is a weak negative correlation.")
        elif -1 < corr < -.5:
            print("That is a strong negative correlation.")
    
    else : 
        print("Fail to reject the null hypothesis.")
    #sns.boxplot(y='tax_value', x ='square_feet', data = train, palette='Set2')
    sns.distplot(train.square_feet, kde=True, color='red')


##################
def age_corr():
    ''' Runs a correlation test between the age of a home and tax valuation,
    plots a box plot'''
    #get data from wrangle
    df = wrangle.get_zillow_data()
    #prepare data from wrangle
    df = wrangle.prepare(df)
    #splits data from wrangle
    train, validate, test = wrangle.split_data(df)
    #State hypothesis: 
    null_hypothesis = "There is no correlation between the age of a home and the tax value"
    alt_hypothesis = "There is a correlation between the age of a home and tax value"
    #alpha
    α = .05
    # set x and y
    x = train.age
    y= train.tax_value
    # run it
    corr, p = stats.pearsonr(x, y)
    print(f' The correlation between the age of a home and the tax value is: {corr:.2f}')
    print(f' The P value between the age of a home and tax value is:  {p:.2f}')
    print(' ')
    if p < α:
        print(f"Reject null hypothesis:\n '{null_hypothesis}'")
        print('\n')
        print(f"We now move forward with our alternative hypothesis: '{alt_hypothesis}'")
        print('\n')
        if 0 < corr < .5:
            print("This is a weak positive correlation.")
        elif .5 < corr < 1:
            print("That is a strong positive correlation.")
        elif -.5 < corr < 0:
            print("This is a weak negative correlation.")
        elif -1 < corr < -.5:
            print("That is a strong negative correlation.")
    
    else : 
        print("Fail to reject the null hypothesis.")
    #sns.boxplot(y='tax_value', x ='square_feet', data = train, palette='Set2')
    sns.distplot(train.age, kde=True, color='red')

    #