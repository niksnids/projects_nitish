#importing libraries
from gensim.utils import dict_from_corpus
import pandas as pd
import numpy as np
from nrclex import NRCLex
import streamlit as st
import pickle
import plotly.express as px
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
st.set_option('deprecation.showPyplotGlobalUse', False)
from gensim.parsing.preprocessing import STOPWORDS, strip_punctuation, strip_short, strip_punctuation
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from functions import clean_data, get_emotion_nrclx, get_emotion_scores, get_top3_emotion_freqs, get_emotion_freqs, get_top_sentences_emotions, _preprocess_text, remove_special_characters
import datetime
from nltk import sent_tokenize
stopwords = set(STOPWORDS)

st.sidebar.header("""
IamHere to show how emotions could be derived from diaries/private journals. 
Choose one blog, period, and a level of analysis.
And do not hesitate to try out your own text.
Enjoy :) 
""")

#dataset (blog) filter for analysis of emotions
blog = st.sidebar.selectbox(label = 'Select the Blog', options=['Diary Blog', 'Travel Blog', 'Depression Blog'])

@st.cache
def load_data(blog):
    if blog == 'Depression Blog':
        df = pickle.load(open('data/depression_marathon_df_final.pkl', 'rb'))
    elif blog == 'Diary Blog':
        df = pickle.load(open('data/george_diary_df_final.pkl','rb'))
    else:
        df = pickle.load(open('data/travel_blog_df_final.pkl', 'rb'))
    df['emotion'] = df.full_text.apply(get_emotion_nrclx) #getting emotions from nrclx library
    return df
df = load_data(blog)

@st.cache
def min_max_dates(df):
    return df.date.min(),df.date.max()
min,max = min_max_dates(df)
st.title("IamHere Dashboard")
period_start = st.sidebar.date_input('Choose the start date for entries', value=datetime.date(2021,3,1), min_value=min, max_value=max)
period_end = st.sidebar.date_input('Choose the end date for entries', min_value=min, max_value=max)
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
#st.sidebar.markdown("**_IamHere to make you understand yourself better. I will show the diary entries and emoions dervied from those entries. Emotions can be analyzed on aggregate level (all entries) and entry level (specific diary entry). For analysis of specific entries, scroll down the dashboard._**")
if period_start > period_end:
    st.error('Error: End date must be after start date.')
#else:
    #st.success('Start date: `%s`\n\nEnd date: `%s`' % (period_start, period_end))
tab = st.sidebar.radio(label = '',options = ('The whole blog', 'A specific post', 'Try out your own text'))

@st.cache
def get_data():
    df_subset = df.loc[(df['date'].dt.date >= period_start) & (df['date'].dt.date < period_end)] #subsetting the data based on user-defined ranges
    df_subset['full_text_clean'] = df_subset.full_text.apply(clean_data).apply(remove_special_characters)
    # df_subset_grouped = df_subset.groupby([pd.Grouper(key='date', freq='7D'), 'emotion']).size().reset_index(name='count') #group by dates and get counts
    freq_list = []
    for i in df_subset.full_text.values:
        emotion_frequencies = get_top3_emotion_freqs(i)
        freq_list.append(emotion_frequencies)
    df_emotion_freq = pd.DataFrame(freq_list)
    df_emotion_freq['date'] = df_subset['date'].values
    df_subset_grouped = df_emotion_freq.groupby([pd.Grouper(key='date', freq='7D')]).mean().reset_index()
    return df_subset,df_emotion_freq,df_subset_grouped
df_subset,df_emotion_freq,df_subset_grouped = get_data()

if tab == 'The whole blog':
    st.write("Number of entries across the specified period:", len(df_subset))
    table = st.write(df_subset[['header','date', 'full_text', 'emotion']])
    #st.write(df_emotion_freq)
    #st.write(df_subset_grouped)

    @st.cache
    def blog_charts():
        #col1, col2 = st.beta_columns((1,2))
        fig1 = px.bar(data_frame=df_subset_grouped, x = 'date', y = df_emotion_freq.columns[df_emotion_freq.columns != 'date'], barmode='group', color_discrete_map= {'positive':'green', 'negative':'red', 'anticipation':'orange', 'trust':'steelblue', 'fear':'purple', 'anger':'indigo', 'surprise': "magenta", 'disgust':'black', 'sadness':'pink', 'joy':'silver'}, title = 'Bar Chart with relative freqency of Emotions for specified time period')
        # fig1 = px.line(data_frame=df_subset_grouped, x = df_subset_grouped.index, y = df_emotion_freq.columns[df_emotion_freq.columns != 'date'], color = 'emotion', color_discrete_map= 
        # {'positive':'steelblue', 'negative':'firebrick', 'anticipation':'orange', 'trust':'green',
        # 'fear':'purple'}, title = 'Bar Chart with dynamics of Emotions for Specified timescale')
        fig1.update_yaxes(title = 'Relative frequency', tickformat = ',.0%')
        fig1.update_xaxes(title = 'weeks')
        agg_avg_emotion_freq = df_subset_grouped.mean()

        agg_sum_emotion_freq = agg_avg_emotion_freq.sum()
        agg_rel_freq_emotion = agg_avg_emotion_freq/agg_sum_emotion_freq
        fig2 = px.pie(names=agg_rel_freq_emotion.index, values=agg_rel_freq_emotion, color = agg_rel_freq_emotion.index, color_discrete_map={'positive':'green', 'negative':'red', 'anticipation':'orange', 'trust':'steelblue', 'fear':'purple', 'anger':'indigo', 'surprise': "magenta", 'disgust':'black', 'sadness':'pink', 'joy':'silver'}, title = 'Pie Chart with relative frequency of Emotions')
        # fig2 = px.pie(data_frame=agg_rel_freq_emotion, names = 'emotion', color= 'emotion', color_discrete_map=
        # {'positive':'steelblue', 'negative':'firebrick', 'anticipation':'orange', 'trust':'green',
        # 'fear':'purple'}, title = 'Pie Chart with frequency of emotions')
        return fig1, fig2
    fig1, fig2 = blog_charts()
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("**_Check Wordcloud showing the most frequent words in the diary entries for the specified time period._**")
    emotion = st.selectbox(label = 'Choose emotion', options = list(df_subset.emotion.unique()))
    
    @st.cache
    def blog_wordcloud():
        #df_subset['full_text_clean'] = df_subset.full_text.apply(clean_data).apply(_preprocess_text)
        df_subset_emotions = df_subset.full_text_clean.loc[df_subset.emotion == emotion]
        df_subset_emotions_text = ''.join(df_subset_emotions)
        
        #plt.figure(figsize=(10,8))
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(df_subset_emotions_text)
        return wordcloud
    wordcloud = blog_wordcloud()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    st.pyplot()
    

    @st.cache
    def top3_sentences():
        df_subset_emotion = df_subset.loc[df_subset.emotion == emotion]
        sent = get_top_sentences_emotions(df_subset_emotion.full_text, emotion_segment=emotion)
        st.markdown('**Top 3 sentences of selected emotion from your diary**', unsafe_allow_html=False)
        st.write('')
        for i in sent[:3]:
            st.write(i)
    top3_sentences()
    st.write('')
    st.write('')

elif tab == 'A specific post':

    ##entry-level filtering section
    #entry_level = st.checkbox(label='Select this to go to the analysis of specific diary entry')
    #if entry_level is True:
    entry_diary = st.selectbox(label='Choose the diary entry', options = list(df_subset.header.unique()))
    df_entry = df.full_text[df.header == entry_diary]
    st.subheader('Diary text')
    #show_diary_entry = st.checkbox(label='Click here to see the full entry of the diary')
    #if show_diary_entry:
    #st.write(df_entry.iloc[0])
    with st.beta_expander("See full blogpost"):
        st.write(df_entry.iloc[0])
    #col1, col2 = st.beta_columns(2)
        #with col1:
            #fig3 = px.pie(data_frame=df_subset_grouped, names = 'emotion', color= 'emotion', color_discrete_map=
            #{'positive':'steelblue', 'negative':'firebrick', 'anticipation':'orange', 'trust':'green',
            #'fear':'purple'}, title = 'Frequency of emotions in the selected entry')
            #st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader('Pie Chart with relative frequency of Emotions in the selected diary entry')
    
    @st.cache
    def post_charts():
        emoji_freq = get_emotion_freqs(df_entry.iloc[0])
        emoji_freq_items = emoji_freq.items()
        data_emojis = list(emoji_freq_items)
        df_emojis = pd.DataFrame(data_emojis,columns = ['Emotion','value'])
        df_emojis_filtered = df_emojis[df_emojis['value'] != 0]
        df_emojis_filtered_list = df_emojis_filtered['Emotion'].tolist()
        fig3 = px.pie(df_emojis_filtered, values= df_emojis_filtered.value, names= df_emojis_filtered_list, color=df_emojis_filtered_list, color_discrete_map={'positive':'green', 'negative':'red', 'anticipation':'orange', 'trust':'steelblue', 'fear':'purple', 'anger':'indigo', 'surprise': "magenta", 'disgust':'black', 'sadness':'pink', 'joy':'silver'})
        return fig3,df_emojis_filtered_list
    fig3,df_emojis_filtered_list = post_charts()
    st.plotly_chart(fig3,use_container_width=True)
        #with col2:

    
    st.subheader('Top words used in the selected diary entry')
    
    @st.cache
    def post_wordcloud():
        df_entry_clean = clean_data(df_entry.iloc[0])
        df_entry_clean = remove_special_characters(df_entry_clean)
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(df_entry_clean)
        return wordcloud
    
    wordcloud = post_wordcloud()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    st.pyplot()  
    st.markdown('**Top 3 sentences of selected emotion from your specified diary entry**')
    emotion = st.selectbox(label = 'Choose emotion', options = df_emojis_filtered_list)
    sent2 = get_top_sentences_emotions(df_entry, emotion)
    for i in sent2:
        st.write(i)
    
    st.write('')
    st.write('')

elif  tab == 'Try out your own text':
    
    abc = """
    We are very excited to show you the result of our work. :)
    We are amazed by the power of NLP and python libraries
    It was not that easy, to be honest. We must admit, there is a lot of stuff to improve. 
    That`s why we need your support to improve what we already have
    """
    message = st.text_area("Just write your text", abc)
    if st.button("Try"):
        col1,col2 =st.beta_columns(2)
        with col1:
            st.subheader('Emotions in your entry')
            blob = get_emotion_freqs(message)
            data_items = blob.items()
            data_list = list(data_items)
            df = pd.DataFrame(data_list,columns = ['Emotion','value'])
            df1= df[df['value'] != 0]
            a_list = df1['Emotion'].tolist()
            fig = px.pie(df1, values= df1.value,names= a_list, color = a_list, color_discrete_map={'positive':'green', 'negative':'red', 'anticipation':'orange', 'trust':'steelblue', 'fear':'purple', 'anger':'indigo', 'surprise': "magenta", 'disgust':'black', 'sadness':'pink', 'joy':'silver'})
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.subheader('Top words used in the text')
            wordcloud2 = WordCloud(background_color='white',width=400, height=200).generate(message)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.imshow(wordcloud2)
            plt.axis("off")
            st.pyplot()
