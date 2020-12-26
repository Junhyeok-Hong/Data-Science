
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **economic activity or measures** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **economic activity or measures**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **economic activity or measures**?  For this category you might look at the inputs or outputs to the given economy, or major changes in the economy compared to other regions.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[1]:

get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.dates as dates
import matplotlib.ticker as ticker


# In[2]:

employment_df = pd.read_csv('Employment Rate (Toronto Residents).csv')
employment_df.drop(['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], axis=1, inplace=True)
employment_df.set_index('Year', inplace=True)
employment_df = employment_df.apply(lambda x: x.str.replace('%', ''), axis=1)
employment_df = employment_df.apply(lambda x: x.astype(float), axis=1)
employment_df.rename(columns={"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6}, inplace=True)
                                    
employment_2020_df = employment_df.T['2020 Actual'] # Final computed series for 2020 employmet rate
employment_df.drop(['2020 Actual'], axis=0, inplace=True)
employment_2010to2019_df = employment_df.mean(axis=0) # Final computed series for 2010 ~ 2019 mean employmet rate


# In[ ]:




# In[3]:

covid19_df = pd.read_excel('CityofToronto_COVID-19_Data.xlsx')
covid19_df['Reported Date'] = pd.to_datetime(covid19_df['Reported Date'])
covid19_df['Reported Date'] = covid19_df['Reported Date'].apply(lambda x: x.strftime('%m-%d'))
covid19_df.sort_values(by=['Reported Date'], ascending=True, inplace=True)
covid19_df.reset_index(drop=True, inplace=True)
covid19_df.drop([], axis=0)
covid19_df.drop(covid19_df[covid19_df['Reported Date'] > '06-30'].index, axis=0, inplace=True)
covid19_df.set_index('Case Count', inplace=True)
covid19_df = covid19_df.apply(lambda x: x.str.replace('-', '.'), axis=1)
covid19_df = covid19_df.apply(lambda x: x.astype(float), axis=1)
covid19_df.reset_index(level=0, inplace=True)
covid19_df.set_index('Reported Date', inplace=True)


# In[4]:

plt.figure()

plt.plot(employment_2010to2019_df, '-', color='blue')
plt.plot(employment_2020_df, '-', color='red')
plt.ylabel('Employment Rate (in %)')
plt.xlabel('Months')
plt.title('Increase in Covid19 Cases vs. Employment Rate \n Toronto, Canada')
plt.legend(['Mean Employment Rate \n 2010~2019', 'Employment Rate \n 2020'], loc=6)
plt.xticks(np.arange(7), ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', "Jun"))

plt2 = plt.twinx()
plt2.plot(covid19_df, '-', color='cyan')
plt.ylabel('Reported Covid19 Cases')
plt.legend(['Covid19 Cases'], loc=6, bbox_to_anchor=(0, 0.365))


# In[ ]:



