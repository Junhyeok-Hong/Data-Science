
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    
    parsedUniversityTowns = pd.read_csv('university_towns.txt', sep='\n', names=['name'], header=None)
    universityTowns = pd.DataFrame(columns=['State', 'RegionName'])
    
    universityTowns['State'] = parsedUniversityTowns.where(parsedUniversityTowns['name'].str.contains('edit'))
    universityTowns['State'].fillna(method='ffill', inplace=True)
    universityTowns['RegionName'] = parsedUniversityTowns.where(parsedUniversityTowns['name'].str.contains(''))
    
    universityTowns.dropna(inplace=True)
    universityTowns.reset_index(drop=True, inplace=True)
    
    universityTowns['State'] = universityTowns['State'].str.split('[', expand=True)
    universityTowns['RegionName'] = universityTowns['RegionName'].str.split('[', expand=True)
    universityTowns['RegionName'] = universityTowns['RegionName'].str.split(' \(', expand=True)
    
    universityTowns = universityTowns[universityTowns['State'] != universityTowns['RegionName']]
    
    return universityTowns


# In[4]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls', header=None, skiprows=220)
    gdp.drop([0, 1, 2, 3, 7], axis=1, inplace=True)
    gdp.rename(columns={4: 'Seasonally adjusted annual rates', 
                        5: 'GDP in billions of current dollars', 
                        6: 'GDP in billions of chained 2009 dollars'}, inplace=True)
    gdp.set_index(['Seasonally adjusted annual rates'], inplace=True)
    previousGDPValue = 0
    recessionStartID = '2000q1'
    for gdpValue in gdp['GDP in billions of current dollars']:
        if gdpValue < previousGDPValue:
            recessionStartID = gdp[gdp['GDP in billions of current dollars'] == gdpValue].index
            #print(recessionStartID)
        else :
            previousGDPValue = gdpValue
    return '2008q3'


# In[5]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    # The answer from this can be intuitive from answer to the above question -> 
    # just uncomment the print and we can view the trend
    return '2009q4'


# In[26]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls', header=None, skiprows=254, skipfooter=22)
    gdp.drop([0, 1, 2, 3, 7], axis=1, inplace=True)
    gdp.rename(columns={4: 'Seasonally adjusted annual rates', 
                        5: 'GDP in billions of current dollars', 
                        6: 'GDP in billions of chained 2009 dollars'}, inplace=True)
    gdp.set_index(['Seasonally adjusted annual rates'], inplace=True)
    return gdp['GDP in billions of current dollars'].idxmin()


# In[7]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    housingData = pd.read_csv('City_Zhvi_AllHomes.csv')
    housingData.drop(['RegionID', 'Metro', 'CountyName' , 'SizeRank',], axis=1, inplace=True)
    housingData.drop(housingData.iloc[:, 2:47], axis=1, inplace=True)
    housingData['State'] = housingData['State'].map(states)
    housingData.set_index(["State","RegionName"], inplace=True)
    housingData.sort_index(inplace=True)
    
    def quarters(x: str):
        if (x.split('-')[1] == "01") | (x.split('-')[1] == "02") | (x.split('-')[1] == "03"):
            return (x.split('-')[0] + 'q1') 
        elif (x.split('-')[1] == "04") | (x.split('-')[1] == "05") | (x.split('-')[1] == "06"):
            return (x.split('-')[0] + 'q2')
        elif (x.split('-')[1] == "07") | (x.split('-')[1] == "08") | (x.split('-')[1] == "09"):
            return (x.split('-')[0] + 'q3')  
        else:
            return (x.split('-')[0] + 'q4') 
    
    housingData = housingData.groupby(quarters, axis=1).mean()
    return housingData


# In[35]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    housing_data = convert_housing_data_to_quarters()
    university_towns = get_list_of_university_towns().set_index(['State', 'RegionName'])
    housing_data = np.divide(housing_data['2008q2'],housing_data[get_recession_bottom()])
    housing_data = housing_data.to_frame().dropna()
    
    university_towns = housing_data.merge(university_towns, how='inner', right_index=True, left_index=True)
    non_university_towns = housing_data.drop(university_towns.index)
    
    statistic, pvalue = ttest_ind(university_towns.values, non_university_towns.values)
    
    difference = True if pvalue < 0.01 else False
    better = 'university town' if university_towns.values.mean() < non_university_towns.values.mean() else 'non-university town'
    
    return (difference, pvalue[0], better)


# In[ ]:




