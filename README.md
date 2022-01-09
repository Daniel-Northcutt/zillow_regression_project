# Predicting Property Valuation in Southern California
### By Daniel Northcutt

<hr style="border:1px solid black"> </hr>

This presentation and notebooks of code should provide strong understanding of the tax value prediction model created.  Following the database pipeline I offer a deep understanding of the Zillow database through exploration and modeling.  All steps can easily be reproduced by following the steps below. This presentation is aimed at helping Zillow understand their data to a deeper level and offer insights in ways to strengthen predictive modeling.

<hr style="border:1px solid black"> </hr>



## Exectuive Summary:
    I created a regression model that beat the baseline model in predicting the 
    tax value of homes in Southern California. The drivers for this model and presentation
    are bedroom count, bathroom count, and square feet while also representing other 
    features in exploration.

## Project Goals:
    - Acquire, prepare, remove outliers, split, and scale the data for actionable means
    - Explore the dataset to create 4 questions to evaluate
    - Provide visual representations, statistical tests, and modeling to aid in 
    understanding the data
    - Use regression modeling to run on our train dataset using multiple features to find 
    the strongest model for predicting tax values
    - Refine and prepare a strong presentation that provides insight clearly and precise

## Background Information:
    - Zillow 2017 Codeup database
    - Single unit properties representing 52,442 homes
    - Counties: Los Angeles, Orange, Ventura
    
<hr style="border:1px solid black"> </hr>

## Questions Asked:
    - Does county location affect tax values?
    - Does the number of bedrooms and/or bathrooms affect tax values?
    - Does the square foot of a home affect the tax value?
    - Is there a relationship between home age and tax value?

<hr style="border:1px solid black"> </hr>

## Skills Used:
    - Python:
        - Pandas
        - Matplotlib
        - Seaborn
        - Numpy
        - Sklearn
    - SQL
    - Statistical Analysis:
        - Descriptive Stats
        - Hypothesis Testing
        - Pearsons r
    - Regression Modeling:
        - Linear Regression Evaluation
        - Tweedie Regressor
        - LassoLars

<hr style="border:1px solid black"> </hr>



## Project Reproduction:
    - Create and use your own env file that connects to the sql database
    - Clone this repo to run on your own make sure to have wrangle.py, explore.py, and 
    evaluate.py with the final report
    - All code is commented in the .py functions along with in the final presentation
    - Use the workbook to explore the prepared data on your own
    
<hr style="border:1px solid black"> </hr>

This project was driven by the desire to dig deep into a dataset to see what can be discoverable.  Through exploration strong understanding of data can be represented and presented.  This project was driven to find what is underneath the hood of a dataset.





# Data Dictionary
| Feature                    | Datatype               | Description                                                           |
|:---------------------------|:-----------------------|:----------------------------------------------------------------------|
| bedroom_count              | 7043 non-null: float   | Bedroom count for homes                 |
| bathroom_count             | 7043 non-null: float   | Bathroom count for homes                    |
| square_feet                | 7043 non-null: float   | Square feet for homes        |
| tax_value                  | 7043 non-null: float   | Tax valuation for homes |
| year_built                 | 7043 non-null: float   | Year the home was built                |
| county                     | 7043 non-null: object  | Represents what county the home resides in        |
| age                        | 7043 non-null: object  | Represents the age of the home                     |
| county_tax_avg             | 7043 non-null: float   | Represents the average tax valuation of  a county             




# Data Dictionary
| Feature                    | Datatype               | Description                                                           |
|:---------------------------|:-----------------------|:----------------------------------------------------------------------|
bathroomcnt                  |          float64
bedroomcnt                   |          float64
calculatedfinishedsquarefeet |          float64
fips                         |          float64
latitude                     |          float64
longitude                    |          float64
lotsizesquarefeet            |          float64
regionidcity                 |          float64
regionidcounty               |           float64
regionidzip                  |           float64
yearbuilt                    |           float64
structuretaxvaluedollarcnt   |           float64
taxvaluedollarcnt            |           float64
landtaxvaluedollarcnt        |           float64
taxamount                    |           float64
county                       |            object
age                          |           float64
age_bin                      |           float64
taxrate                      |           float64
acres                        |           float64
acres_bin                    |           float64
sqft_bin                     |           float64
structure_dollar_per_sqft    |           float64
structure_dollar_sqft_bin    |           float64
land_dollar_per_sqft         |           float64
lot_dollar_sqft_bin          |           float64
bath_bed_ratio               |           float64
cola                         |             int64
logerror_bins                |          category
baseline                     |           float64
scaled_latitude              |           float64
scaled_longitude             |           float64
scaled_bathroomcnt           |           float64
scaled_taxrate               |           float64
scaled_bedroomcnt            |           float64
scaled_lotsizesquarefeet     |           float64
scaled_age                   |           float64
scaled_acres                 |           float64
scaled_bath_bed_ratio        |           float64
scaled_calculatedfinishedsquarefeet|     float64
area_cluster                 |            object
size_cluster                 |            object
price_cluster                |            object
tax_cluster                  |            object
area_cluster_la_newer        |             uint8
area_cluster_la_older        |             uint8
area_cluster_northwest_costal|             uint8
area_cluster_palmdale_landcaster |         uint8
area_cluster_santa_clarita   |             uint8
area_cluster_se_coast        |             uint8
size_cluster_1250_to_1650    |             uint8
size_cluster_1300_to_2000    |             uint8
size_cluster_1500_to_1900    |             uint8
size_cluster_1500_to_2800    |             uint8
size_cluster_2300_to_4400    |             uint8
size_cluster_2900_to_4000    |             uint8
size_cluster_900_to_1200     |             uint8
price_cluster_144000_to_355000|            uint8
price_cluster_34000_to_110000 |            uint8
price_cluster_420000_to_870000|            uint8
price_cluster_45000_to_173000 |            uint8
price_cluster_69000_to_210000 |            uint8
tax_cluster_1000_to_3000      |            uint8
tax_cluster_16000_to_22000    |            uint8
tax_cluster_30000_to_40000    |            uint8
tax_cluster_5000_to_6000      |            uint8
tax_cluster_8500_to_12000     |            uint8
logerror                      |          float64



