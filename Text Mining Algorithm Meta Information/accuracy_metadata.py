#!/usr/bin/env python
# coding: utf-8

# In[12]:


from os import listdir
from os.path import isfile, join
from tabulate import tabulate
from tika import parser 
import pprint
import pandas as pd
import meta_information_class
import numpy as np
from collections import Counter
import os
import glob


# In[53]:


accuracy_df = pd.read_csv(r'C:\Users\nitis\OneDrive\Dokumente\GitHub\signavio_project\accuracy test.csv',sep=',')
def accuracy_documents():
# get only the data of the file 
    y =accuracy_df.loc[accuracy_df['doc'].isin([file2])]
# get the rows with particular meta data
    y =y.loc[y['meta information'].isin(['documents'])].reset_index(drop=True)
# put it in the list
    data_manual = y['value'].to_list()
    data_manual = [x.replace(' ', '') for x in data_manual]
    data_manual = [each_string.lower() for each_string in data_manual]
# count the items in the list
    count_manual=len(data_manual)
    a= information_df.loc[information_df['meta information'].isin(['documents'])]
    a = a.loc[a['doc'].isin([file2])]
    a = a.drop(['count'], axis=1)
    a = a[["value"]].reset_index(drop=True)
    list_of_x = a['value'].to_list()
    list_of_x = [x.replace(' ', '') for x in list_of_x]
    list_of_x = [each_string.lower() for each_string in list_of_x]
    count_class = len(list_of_x)
    intersectoin = list(set(data_manual) & set(list_of_x))
    count_same = len(intersectoin)
    accuracy = count_same/count_manual
    return (accuracy)

def accuracy_date():
    # get only the data of the file 
    y =accuracy_df.loc[accuracy_df['doc'].isin([file2])]
# get the rows with particular meta data
    y =y.loc[y['meta information'].isin(['date'])].reset_index(drop=True)
# put it in the list
    data_manual = y['value'].to_list()
    data_manual = [x.replace(' ', '') for x in data_manual]
    data_manual = [each_string.lower() for each_string in data_manual]
# count the items in the list
    count_manual=len(data_manual)
    a= information_df.loc[information_df['meta information'].isin(['date'])]
    a = a.loc[a['doc'].isin([file2])]
    a = a.drop(['count'], axis=1)
    a = a[["value"]].reset_index(drop=True)
    list_of_x = a['value'].to_list()
    list_of_x = [x.replace(' ', '') for x in list_of_x]
    list_of_x = [each_string.lower() for each_string in list_of_x]
    count_class = len(list_of_x)
    intersectoin = list(set(data_manual) & set(list_of_x))
    count_same = len(intersectoin)
    accuracy = count_same/count_manual
    return (accuracy)

def linked_processess():
    # get only the data of the file 
    y =accuracy_df.loc[accuracy_df['doc'].isin([file2])]
# get the rows with particular meta data
    y =y.loc[y['meta information'].isin(['linked processes'])]
    y= y.reset_index(drop=True)
# put it in the list
    data_manual = y['value'].to_list()
    data_manual = [x.replace(' ', '') for x in data_manual]
    data_manual = [each_string.lower() for each_string in data_manual]
# count the items in the list
    count_manual=len(data_manual)
    a= information_df.loc[information_df['meta information'].isin(['linked processes'])]
    a = a.loc[a['doc'].isin([file2])]
    a = a.drop(['count'], axis=1)
    a = a[["value"]]
    a= a.reset_index(drop=True)
    list_of_x = a['value'].to_list()
    list_of_x = [x.replace(' ', '') for x in list_of_x]
    list_of_x = [each_string.lower() for each_string in list_of_x]
    count_class = len(list_of_x)
    intersectoin = list(set(data_manual) & set(list_of_x))
    count_same = len(intersectoin)
    accuracy = count_same/count_manual
    return (accuracy)

def name():
    # get only the data of the file 
    y =accuracy_df.loc[accuracy_df['doc'].isin([file2])]
# get the rows with particular meta data
    y =y.loc[y['meta information'].isin(['name'])].reset_index(drop=True)
# put it in the list
    data_manual = y['value'].to_list()
    data_manual = [x.replace(' ', '') for x in data_manual]
    data_manual = [each_string.lower() for each_string in data_manual]
# count the items in the list
    count_manual=len(data_manual)
    a= information_df.loc[information_df['meta information'].isin(['name'])]
    a = a.loc[a['doc'].isin([file2])]
    a = a.drop(['count'], axis=1)
    a = a[["value"]].reset_index(drop=True)
    list_of_x = a['value'].to_list()
    list_of_x = [x.replace(' ', '') for x in list_of_x]
    list_of_x = [each_string.lower() for each_string in list_of_x]
    count_class = len(list_of_x)
    intersectoin = list(set(data_manual) & set(list_of_x))
    count_same = len(intersectoin)
    accuracy = count_same/count_manual
    return (accuracy)


# In[54]:


filenames = [f for f in listdir('data_accuracy') if isfile(join('data_accuracy', f))]
file_idx = 2
file = 'data_accuracy/'+filenames[file_idx]
file


# In[55]:


raw = parser.from_file(file)
text = raw["content"]


# In[56]:


keywords_names_list = ['procedure', 'process', 'sop', 'policy', 'manual', 'step']
keywords_documents_list = ['purchase', 'order', 'form', 'request', 'invoice', 'documents', 'document', 'documentation']
keywords_date_list = ['issued date','issue-date','effective-date', 'implementation-date','updated', 'adopted' ,'revised',"review date","revision date","version","last revision","issued","effective date","date"]


# In[57]:


information = meta_information_class.extract_meta_information(file, keywords_names_list, keywords_date_list, keywords_documents_list)
information_dict = information.create_dict()
information_df = information.create_df()


# In[58]:


information_df ['doc'] = file.replace('data_accuracy/','')
information_df ['meta information'] = information_df ['meta information'].replace('documents (2-gram)','documents')
information_df ['meta information'] = information_df ['meta information'].replace('documents (3-gram)','documents')
information_df ['meta information'] = information_df ['meta information'].replace('effective date','date')
information_df ['meta information'] = information_df ['meta information'].replace('last revision','date')
information_df ['meta information'] = information_df ['meta information'].replace('adopted','date')
information_df ['meta information'] = information_df ['meta information'].replace('revised','date')
information_df ['meta information'] = information_df ['meta information'].replace('version','date')
information_df ['meta information'] = information_df ['meta information'].replace('issued date','date')
information_df ['meta information'] = information_df ['meta information'].replace('revision date','date')


# In[59]:


#extract the file name in order to get the data only relavant to the file name
file1 =file
file2 = file1.replace('data_accuracy/','')
file2


# # ACCURACY

# In[60]:


def accuracy():
    linked_process = linked_processess()
    date = accuracy_date()
    document= accuracy_documents()
    names = name()
    return [date,linked_process,document,names]    


# In[61]:


result3 = accuracy()
accuracy = pd.DataFrame(result3).transpose()
accuracy1 = accuracy.rename(columns={0: 'Date', 1: 'linked_process', 2:'documents',3:'names'})
accuracy1


# 
# Process:
# (1) Manually created excel sheet with 8 random process documents with meta data similar to what we are extracting
# 
# (2) Compare the list of what our class extracted and what i manually inserted. Eg: Is the extracted metadata is in the list of manually inserted metadata
# 
# (3) check how accurately are we extracting the meta data
# 
# Note: Sometimes there are no linked process in documents so the accuracy is always 100 %
# Some pdf were really long so i might have missed some document names or linkes processses
# 
# Positive:
# For date and process name, it is more accurate than other meta data
# 
# 
# Challenges:
# 
# (1) Some name of documents are more that 3 words so bigram and trigram might not provide accurate name
# Example:   Flow projection form == cash flow projection form
#            Dispute resolution form =  Complaints and Disputes Resolution Form 
# 
# (2) Some extracted documents are not actually documents 
# example: list of documents: its not acually document but its just a context in a sentence.
#  1. List of documents that will be cancelled upon issuance of this 
# 
# 
# Next step: Try to enhance the code so that we can increase the accuracy. 
# Loop over and put in a matrix for all documents
# 

# In[ ]:




