#!/usr/bin/env python
# coding: utf-8

# In[39]:


from tika import parser 
import re
from collections import Counter
import spacy
nlp = spacy.load("en_core_web_sm")
import PyPDF2 as pypdf
from textblob import TextBlob
import pandas as pd
from pandas import DataFrame
import datefinder
from datetime import date


# In[40]:


def calcu (x):
    # This function is used to find date from the string
    matches = datefinder.find_dates(x)
    for match in matches:
        return match

def extract_date (text):
    # This function is used to find diffenet date attributes in the process documents
    try: 
        # created list of keywords tha are realted to date values
        keywords = ["issued date","issue-date","effective-date", "implementation-date","updated", "adopted" ,"revised","review date","revision date","version","last revision","issued","effective date","date"]
        
        # searched those keywords in each line and return only those lines
        header = [ t for t in text.split('\n') if any([key in t for key in keywords])]
        
        #Put the output in a dataframe with keywords and the date value that it corresponds to
        df = DataFrame(header,columns=['content'])
        
        #Only keep the rows that has atleast 2 digit numbers in the content column
        df = df[df['content'].str.contains('\d\d')]
        
        # delete all the duplicates
        df=df.drop_duplicates(subset=None, keep='first', inplace=False)
        
        # create a column that shows the keywords which corresponds to the date value
        df['EXTRACT'] = df.content.str.extract('({})'.format('|'.join(keywords)), flags=re.IGNORECASE, expand=False).str.lower().fillna('')
        
        # Just keep the rows that has value in the column 
        df=df[df.EXTRACT != ''] 
        
        #Create a date column that has value after the word in the column Extract
        df['Date']=df.apply(lambda x: x['content'].split(x['EXTRACT'])[1], axis=1)
        
        #Drop the table content
        df=df.drop('content',axis=1)
        
        # needs to be modified . jus tfor one use case
        df['Date'] = [x.split('last revision')[0] for x in df['Date']]
        df = df[df['Date'].str.contains('\d\d')]
        
        # we use function calcu
        df['Date'] = df.Date.apply(calcu)
        
        df=df.drop_duplicates(subset=None, keep='first', inplace=False).sort_values(['Date'], ascending=[True]).reset_index(drop = True)
        df['Date'] = df['Date'].dt.date
        today = date.today()
        
        # date should be less than today because the datefinder sometimes take any numbers and give a random dates
        df = df[(df['Date'] <= today)]
        
        return(df)
    except:
        return(calcu(text))


# In[41]:


file_vec = ["04_SOP-Business-Plan.pdf","investigation-procedure.pdf","AccountsPayablePolicy.pdf","accounts-payable-policy-procedures.pdf","ID_IZ_INFOHCP_S&H_VaccineManagementPlan.pdf","FIN-ACP-001.pdf","FINA_Accounts_Payable.pdf","Tendering_Process_Advice.pdf","322687main_ITS-SOP-0004-A-NASA-NITR-Procedures.pdf","AIDSRelief+Supply+Chain+Manual.pdf"]


# In[55]:


file_index = 3
raw = parser.from_file("C:/Users/nitis/OneDrive/Desktop/TWSM/Process documents/"+file_vec[file_index])
text = raw["content"]
text = text.strip()
text = text.replace('  ', '')
text = text.replace(' \n',' ')
text=text.lower()


# In[56]:


result = extract_date(text)
result


# In[57]:


datefinal = dict((result.values.tolist()))
datefinal


# Challenges
# 
# (1) Date like : 20101202
# In this point where we want to have uniform date format, this function (date finder)  was not able to work with this sort of values. 
# 
# We can look into other function but i dint find any other useful one or  use a regex function for date.
# 
# 
# 
# (2)	Keywords and date in different lines : Our approach is to take the keywords and the value in a line but there are instances where keywords and value are in different line.  Almost 9 out of 10 documents have keywords and value in same line.

# In[ ]:





# In[ ]:




