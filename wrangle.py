## ORDER:

# - Imports
# - Acquire
# - CSV & Function
# - Drop Columns
# - Rename Columns
# - Remove Duplicates
# - Convert Datatypes
# - Split it right
# - Remove Outliers
# - Wrangle it up




#******************* IMPORTS ***********************

import pandas as pd
import numpy as np
import os
from env import host, user, password
from sklearn.model_selection import train_test_split
import sklearn.preprocessing


#******************* ACQUIRE  ***********************
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

#******************* SQL QUERY IMPORT ***********************

# note: I did not add taxamount

def new_zillow_data():
    '''
    This function reads the Bed/Bath count, Finished Sq Ft, Taxable Value, Year Built, and Amount Taxed
    from the 2017 Properties Zillow data from the Codeup SQL server into a df.
    '''
    sql_query = """
                SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, 
                taxvaluedollarcnt, yearbuilt, fips, transactiondate
                FROM properties_2017
                JOIN propertylandusetype USING(propertylandusetypeid)
                JOIN predictions_2017 USING(parcelid)
                WHERE propertylandusetype.propertylandusetypeid = 261 AND 279;
                """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df


#******************* GET THE DATA & CREATE CSV ***********************


def get_zillow_data():
    '''
    This function reads in zillow data from the Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_zillow_data()
        
        # Cache data
        df.to_csv('zillow.csv')
        
    return df
#### Prepare ###
#******************* Remove Outliers ***********************


def remove_outliers(df, k, col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and return that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df


def prepare(df):
    '''
    Takes a zillow df as an argument and returns a df with handled nulls, removed nulls, changed column types,
    drop duplicates, and remove outliers. Drops taxamount to avoid data leak.
    '''
    #Rename columns
    df = df.rename(columns = {'bedroomcnt':'bedrooms', 
                            'bathroomcnt':'bathrooms', 
                            'calculatedfinishedsquarefeet':'area',
                            'taxvaluedollarcnt':'tax_value', 
                            'yearbuilt':'year_built',
                            'transactiondate': 'transaction_date'})
    # col_list for outliers
    col_list = ['bedrooms', 'bathrooms', 'area', 
            'tax_value', 'year_built', 'fips']
    # run df through remove_outliers function for all columns
    df = remove_outliers(df, 1.5, col_list)
    
    # drop duplicates
    df.drop_duplicates()

    # for loop to change dtypes of appropriate columns to int
    for col in df.columns[df.columns != 'transaction_date']:
        df[col] = df[col].astype(int)

    return df



#******************* SPLIT DATA ***********************


def split_data(df):
    '''
    Takes in a dataframe and returns train, validate, and test subset dataframes. 
    '''
    train, test = train_test_split(df, test_size = .2, random_state = 222)
    train, validate = train_test_split(train, test_size = .3, random_state = 222)
    return train, validate, test

#******************* SCALE DATA ***********************


def scale_zillow(train, validate, test):
    '''
    Takes train, validate, test datasets as an argument and returns the dataframes with 
    tax_vale, and area scaled columns.
    '''
    ## MinMaxScaler
    scaler = sklearn.preprocessing.MinMaxScaler()

    # Fit scaler to data
    scaler.fit(train[['tax_vale', 'area']])

    # Execute scaling
    train[['area', 'tax_value_scaled']] = scaler.transform(train[['area', 'tax_value']])
    validate[['area_scaled', 'tax_value_scaled']] = scaler.transform(validate[['area', 'tax_value']])
    test[['area_scaled', 'tax_value_scaled']] = scaler.transform(test[['area', 'tax_value']])
    return train, validate, test


#******************* Wrangle it up ***********************

def wrangle_zillow():
    '''Combines are previous functions by acquire, cleaning, and splitting data'''

    #Acquire
    df = get_zillow_data()
    
    #Prepare
    df = prepare(df)
    
    #Splits
    train, validate, test = split_data(df)

    #Scale it out
    train, validate, test, = scale_zillow(train, validate, test)

    return train, validate, test