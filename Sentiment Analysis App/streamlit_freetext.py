#!/usr/bin/env python
# coding: utf-8

# In[5]:


from mpl_toolkits.mplot3d import Axes3D
#from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from nrclex import NRCLex
from matplotlib.font_manager import FontProperties
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS


# In[6]:

def calcu1 (x):
    text_object = NRCLex(x)
    matches = text_object.affect_frequencies
    return (matches)    

abc = 'I am walking in the forest. I just saw a lion. I was scared and surprised. I was not sure what to do'

if  st.subheader("Write down your thoughts"):
    
    message = st.text_area("Enter Text",abc)

    if st.button("Submit"):
         col1,col2 =st.beta_columns(2)
         with col1:
           st.subheader('Frequency of your emotions')
           blob = calcu1(message)
           data_items = blob.items()
           data_list = list(data_items)
           df = pd.DataFrame(data_list,columns = ['Emotion','value'])
           df1= df[df['value'] != 0]
           a_list = df1['Emotion'].tolist()
           fig = px.pie(df1, values= df1.value,names= a_list)
           st.plotly_chart(fig,use_container_width=True)
         with col2:
           st.subheader('Top words used in the text')
           wordcloud2 = WordCloud(background_color='white',width=400, height=200).generate(message)
           st.set_option('deprecation.showPyplotGlobalUse', False)
           plt.imshow(wordcloud2)
           plt.axis("off")
           st.pyplot()




# In[7]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




