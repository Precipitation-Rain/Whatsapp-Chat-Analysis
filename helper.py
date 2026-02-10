from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji 
cloud = WordCloud()
extractor  = URLExtract() 

def Fetch_Stats(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    #Fecthing num of messages
    num_messages = df.shape[0]

    # no of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # media messages
    num_media_messages = df[df['Message'] == '<Media omitted>'].shape[0]

    # no of links
    link = []
    for message in df['Message']:
        link.extend(extractor.find_urls(message))


    return num_messages , len(words) , num_media_messages , len(link)

def Most_Busy_Person(df):

    # most busy users
    x = df['User'].value_counts().head()

    # chat percentage
    df = round(( df['User'].value_counts() / df.shape[0] )*100 , 2).reset_index().rename(columns = {'User':'Name','count':'Percentage'})

    return x , df

def create_worcloud(selected_user , df):

    f = open('marathi_english_hinglish_stopwords.txt','r',encoding="utf-8")
    stop_words = f.read()  

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['Message'] != '<Media omitted>']
    temp = temp[temp['User'] != 'System']

    def remove_stop_words(message):
        clean = []
        for word in message.lower().split():
            if word not in stop_words:
                clean.append(word) 
        return "".join(clean)

    wc = WordCloud(width = 500 , height = 500 , min_font_size = 10 , background_color = 'white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep = " "))

    return df_wc

def most_common_words(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['Message'] != '<Media omitted>']
    temp = temp[temp['User'] != 'System']

    f = open('marathi_english_hinglish_stopwords.txt','r',encoding="utf-8")
    stop_words = f.read()


    words = []
    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

   
    most_coomon_words_df = pd.DataFrame(Counter(words).most_common(20))

    return most_coomon_words_df
    
def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []

    for msg in df['Message']:
        for char in msg:
            if emoji.is_emoji(char):
                emojis.append(char)

    total_emojis = len(emojis)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df , total_emojis

def monthly_timeline(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year','month_num','Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + " - " + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline

def weekly_activity_map(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap

