#!/usr/bin/env python3

# author: Jeff Morin
# email: morin.jeff@gmail.com
# date: 07/14/2020

# This script pulls in the data, cleans then transforms the data to be used for analysis

import datetime
import pandas as pd
import numpy as np



def load_data(file):
    ''' load the data into a pandas dataframe'''
    return pd.read_csv(file)


def clean_data(df, cols_to_drop, cols_to_fill, new_cols, cols_to_split):
    '''cleans up the data to be useful for analysis'''

    # Drop unnecessary columns
    df.drop(columns=cols_to_drop1, axis=1, inplace=True)

    # Drop duplicates based on 'ID'
    df_clean = df.drop_duplicates(subset='ID')

    # Impute missing values as 'Unknown'
    df_clean[cols_to_fill] = df_clean[cols_to_fill].fillna(str('Unknown'))

    # Create new columns from splitting a column
    df_clean[new_cols] = df_clean[cols_to_split].str.rsplit(
        '\n', expand=True, n=2)
    df_clean[new_cols[0]] = df_clean[new_cols[0]
                                     ].str.split(',', expand=True, n=2)
    df_clean[new_cols[0]] = df_clean[new_cols[0]].str.upper()
    return df_clean


def transform_data(df, sex_category, race_category, drugs):
    # Create the new time units
    df['Date'] = pd.to_datetime(df.Date)
    df['week'] = df['Date'].dt.week
    df['month'] = df['Date'].dt.month
    df['month_name'] = df['Date'].dt.month_name()
    df['year'] = df['Date'].dt.year
    
    # imputing the median for 'Age'
    df['Age'] = df['Age'].fillna((df['Age'].median()))
    
    # create new column with age bins from 'Age'
    df['Age_Bin'] = pd.cut(df['Age'], [0, 14, 24, 34, 44, 54, 64, 74, 84, 115],
                       labels=['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+'])

    # Recode 'Sex' change to Categorical
    df['Sex_Cat'] = df['Sex'].replace(sex_category)
    df['Sex_Cat'] = df['Sex_Cat'].astype('category')

    # Recode race to Categorical
    df['Race_Cat'] = df['Race'].replace(race_category)
    df['Race_Cat'] = df['Race_Cat'].astype('category')

    # Change all drug columns values to either 1 (has value) or 0 (is null)
    for d in drugs:
        df[d] = np.where(df[d].notnull(), 1, 0)
        df[d] = df[d].astype('category')
    return df


def new_columns(df, opioids):
    '''Create new columns for different classes of opioids'''

    for o in opioids.items():
        col_name = o[0]
        vals = o[1]
        df[col_name] = 0
        for v in vals:
            mask = (df[v] == 1)
            df[col_name] = df[col_name].mask(mask, 1)
            df[col_name] = df[col_name].astype('category')
    return df


def get_city_county(df, df2, cols_to_drop, cols_to_rename):
    '''Prepare city/county dataframe, then merge with main data 
        to get complete list of cities and GeoLocations'''

    # Convert city and county to uppercase
    df2['County'] = df2['County'].str.upper()
    df2['City'] = df2['City'].str.upper()

    # Create a dictionary of cities and counties
    city_county_dict = pd.Series(
        df2['County'].values, index=df2['City']).to_dict()

    # merging the data on 'city'
    df = pd.merge(df, df2, on=['City'], how='outer')

    # Create a new df with 'DeathCity' and 'DeathCounty', drop NaN's and convert to dictionary
    deathcity_deathcounty = df.loc[:, ['DeathCity', 'DeathCounty']]
    deathcity_deathcounty.dropna(inplace=True)
    deathcity_deathcounty_dict = pd.Series(
        deathcity_deathcounty['DeathCounty'].values, index=deathcity_deathcounty['DeathCity']).to_dict()

    # join the two dictionairies, remake into a dataframe for merging
    all_city_county_dict = {**deathcity_deathcounty_dict, **city_county_dict}
    df_city_county = pd.DataFrame.from_dict(
        all_city_county_dict, orient='index')
    df_city_county = df_city_county.reset_index()
    df_city_county.rename(columns={'index': 'City', 0: 'County'}, inplace=True)

    # merging the city/county data with the main data
    df = pd.merge(df, df_city_county, on=['City'], how='outer')
    
    # Drop unnecessary columns
    df.drop(columns=cols_to_drop, axis=1, inplace=True)
    
    # Rename columns
    df.rename(columns=cols_to_rename, inplace=True)

    return df


def data_cleanup(df, col_order):
    # Drop all extra rows with no 'ID'
    df.dropna(subset=['ID'], inplace=True)

    # Reorganize all the rows by kind
    df = df[col_order]
    
    return df
    

def error_correction(df, corrections, date_correction):

    # correcting specific user entry errors
    for c in corrections:
        df.loc[df['ID']==c[0],'DeathCity'] = c[1]
        df.loc[df['ID']==c[0],'DeathCounty'] = c[2]

    for d in date_correction:
        new_date = pd.to_datetime(d[1])
        df.loc[df['ID']==d[0],'Date'] = new_date
        df.loc[df['ID']==d[0],'week'] = d[2]
        df.loc[df['ID']==d[0],'month'] = d[3]
        df.loc[df['ID']==d[0],'month_name'] = d[4]
        df.loc[df['ID']==d[0],'year'] = d[5]
    
    return df

    

if __name__ == '__main__':

    # Define inputs
    CT_Overdoses = "data/Accidental_Drug_Related_Deaths_2012-2018.csv"
    CT_Cities_Counties = "data/CT_Cities_Counties.csv"

    # Define variables
    cols_to_drop1 = ['DateType', 'ResidenceCity', 'ResidenceCounty', 'ResidenceState', 'InjuryCity',
                     'InjuryCounty', 'InjuryState', 'OtherSignifican', 'MannerofDeath', 'ResidenceCityGeo', 'InjuryCityGeo'
                    ]

    cols_to_fill = ['Sex', 'Race']

    cols_to_split = 'DeathCityGeo'

    new_cols = ['City', 'DeathGeo']

    sex_category = {'Female': 0, 'Male': 1, 'Unknown': 2}

    race_category = {'Asian Indian': 1, 'Asian, Other': 2, 'Black': 3, 'Chinese': 4, 'Hawaiian': 5,
                     'Hispanic, Black': 6, 'Hispanic, White': 7, 'Native American, Other': 8, 'White': 9, 'Other': 0, 'Unknown': 0
                     }

    drugs = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone',
             'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad',
             'Morphine_NotHeroin', 'Hydromorphone', 'OpiateNOS'
             ]

    opioids = {'opioid_nat': ['Oxycodone', 'Oxymorphone', 'Hydrocodone', 'Methadone', 'Morphine_NotHeroin', 'Hydromorphone'],
               'opioid_synt': ['Fentanyl', 'FentanylAnalogue', 'Tramad', 'OpiateNOS'],
               'opioid_not_heroin': ['Oxycodone', 'Oxymorphone', 'Hydrocodone', 'Methadone', 'Morphine_NotHeroin', 'Hydromorphone',
                                     'Fentanyl', 'FentanylAnalogue', 'Tramad', 'OpiateNOS']
               }

    cols_to_rename = {'City': 'DeathCity', 'DeathGeo': 'DeathCityGeo', 'County_y': 'DeathCounty'}

    cols_to_drop2 = ['DeathCounty', 'DeathCity', 'DeathCityGeo', 'County_x']

    col_order = ['ID', 'Date', 'week', 'month', 'month_name', 'year','Age', 'Age_Bin', 'Sex',
                 'Sex_Cat', 'Race', 'Race_Cat','DeathCity', 'DeathCityGeo', 'DeathCounty',
                 'Location', 'LocationifOther', 'InjuryPlace','DescriptionofInjury','COD',
                 'Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue','Oxycodone', 'Oxymorphone',
                 'Ethanol','Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 
                 'Morphine_NotHeroin','Hydromorphone', 'Other', 'OpiateNOS','AnyOpioid',
                 'opioid_nat', 'opioid_synt', 'opioid_not_heroin'
                ]
    
    corrections =[['14-028', 'WEST HAVEN', 'NEW HAVEN'],
                  ['14-0043', 'EAST WINDSOR', 'HARTFORD'],
                  ['16-0690', 'EAST WINDSOR', 'HARTFORD'], 
                  ['15-0472', 'NEW CANAAN', 'FAIRFIELD'],
                  ['17-0206', 'GROTON', 'NEW LONDON']
                 ]
    
    date_correction = [['15-0728','2015-12-31',53,12,'December',2015],
                       ['15-0729','2015-12-31',53,12,'December',2015]
                      ]


    # Load data
    df_overdose = load_data(CT_Overdoses)
    df2 = load_data(CT_Cities_Counties)

    # Clean data
    df_cleaned = clean_data(df_overdose, cols_to_drop1,
                            cols_to_fill, new_cols, cols_to_split)

    # Transform data
    df_transformed = transform_data(
        df_cleaned, sex_category, race_category, drugs)

    # Add columns for opioid type
    df = new_columns(df_transformed, opioids)

    # Merge city and county data with main data
    df = get_city_county(df, df2, cols_to_drop2,cols_to_rename)
                        
     # line item corrections to data errors 
    df_final = error_correction(df, corrections, date_correction)
    
    # cleanup of the data: dropping , renaming, adjusting types, etc
    df = data_cleanup(df, col_order)

    
    #df.info()
    # save to csv for inspection
    #df.to_csv(r"data/Clean_Transformed_Accidental_Drug_Related_Deaths_2012-2018.csv", index=False)
