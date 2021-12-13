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


####
def prepare(df):
    '''
    Takes a zillow df as an argument and returns a df removed nulls, changed column names & types,
    drop duplicates, and remove outliers.
    '''
    #Rename columns
    df = df.rename(columns = {'bedroomcnt':'bedroom_count', 
                            'bathroomcnt':'bathroom_count', 
                            'calculatedfinishedsquarefeet':'square_feet',
                            'taxvaluedollarcnt':'tax_value', 
                            'yearbuilt':'year_built',
                            'transactiondate': 'transaction_date',
                            'fips': 'county'})
    # Rename fips numbers to the county associated
    df['county'] = df['county'].replace({6037.0:'LA',6059.0: 'Orange',6111.0:'Ventura'})

    col_list = ['bedroom_count', 'bathroom_count', 'square_feet','tax_value', 'year_built']
    df = remove_outliers(df, 1.5, col_list)

    # drop duplicates
    df.drop_duplicates()

    #Age column
    from datetime import date
    df['age'] = date.today().year-df['year_built']

    dummy_df = pd.get_dummies(df[['county']], drop_first = True)
    df = pd.concat([df, dummy_df], axis = 1)


    return df
#******************* COUNTY AVGS ***********************

# Note did not use in presentation - great feature to explore further
def county_avg(df):
    ''' This function creates a county avg price'''
    LA = df[df.county=='LA']
    orange = df[df.county=='Orange']
    ventura = df[df.county=='Ventura']

    la_avg = round(LA.tax_value.mean(),2)
    orange_avg = round(orange.tax_value.mean(),2)
    ventura_avg = round(ventura.tax_value.mean(),2)

    def assign_county_avg(row):
        if row['county']=='LA':
            return la_avg
        if row['county']=='Orange':
            return orange_avg
        if row['county']=='Ventura':
            return ventura_avg
    df['county_tax_avg'] = df.apply(lambda row: assign_county_avg(row), axis = 1)

    return df


#******************* SPLIT DATA ***********************


def split_data(df):
    '''
    Takes in a dataframe and returns train, validate, and test subset dataframes. 
    '''
    train, test = train_test_split(df, test_size = .2, random_state = 222)
    train, validate = train_test_split(train, test_size = .3, random_state = 222)
    return train, validate, test

#******************* Baseline ***********************
def add_baseline(train, validate, test):
    ''' Baseline by mean for train, validate, and test'''
    baseline = train.tax_value.mean()
    train['baseline'] = baseline
    validate['baseline'] = baseline
    test['baseline'] = baseline
    return train, validate, test



#******************* SCALE DATA ***********************


def scale_zillow(train, validate, test):
    '''
    Takes train, validate, test datasets as an argument and returns the dataframes with 
    tax_value, and square_feet scaled columns.
    '''
    ## MinMaxScaler
    scaler = sklearn.preprocessing.MinMaxScaler()

    # Fit scaler to data
    scaler.fit(train[['tax_value', 'square_feet', 'bedroom_count', 'bathroom_count']])

    # Execute scaling
    train[['square_feet_scaled', 'tax_value_scaled', 'bedroom_count_scaled', 'bathroom_count_scaled']] = scaler.transform(train[['square_feet', 'tax_value', 'bedroom_count', 'bathroom_count']])
    validate[['square_feet_scaled', 'tax_value_scaled', 'bedroom_count_scaled', 'bathroom_count_scaled']] = scaler.transform(validate[['square_feet', 'tax_value', 'bedroom_count', 'bathroom_count']])
    test[['square_feet_scaled', 'tax_value_scaled', 'bedroom_count_scaled', 'bathroom_count_scaled']] = scaler.transform(test[['square_feet', 'tax_value', 'bedroom_count', 'bathroom_count']])
    return train, validate, test


#******************* Wrangle it up ***********************

def wrangle_zillow():
    '''Combines are previous functions by acquire, cleaning, and splitting data'''

    #Acquire
    df = get_zillow_data()
    
   #Prepare
    #df = prepare(df)

    #Remove Outliers

    #df = remove_outliers(df, 1.5, ['bedroom_count', 'bathroom_count', 'square_feet','tax_value'])

    #Prepare
    df = prepare(df)
    
    #County Avg
    df = county_avg(df)

    #Splits
    train, validate, test = split_data(df)

    #Baseline
    train, validate, test = add_baseline(train, validate, test)

    #Scale it out
    train, validate, test, = scale_zillow(train, validate, test)

    return train, validate, test