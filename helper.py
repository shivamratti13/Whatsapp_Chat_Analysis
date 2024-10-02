from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch number of messages
    num_messages = df.shape[0]

    # number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    # number of Media Shared
    media_shared = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # number of links/urls
    extractor = URLExtract()
    links = []
    for message in df['messages']:
        links.extend(extractor.find_urls(message))
    

    return num_messages,len(words),media_shared,len(links)


def fetch_most_active_users(df):
    x = df['users'].value_counts().head()
    new_df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index()
    new_df = new_df.rename(columns = {'users':'users','count':'percent'})
    return x,new_df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['messages'] != '<media']
    temp = temp[temp['messages'] != 'omitted>']
    temp = temp[temp['messages'] != 'omitted>\n']
    temp = temp[temp['messages'] != '<Media']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != '<media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)

    wc = WordCloud(width = 500, height=500, min_font_size = 10, background_color = 'white')
    temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['messages'] != '<media']
    temp = temp[temp['messages'] != 'omitted>']
    temp = temp[temp['messages'] != 'omitted>\n']
    temp = temp[temp['messages'] != '<Media']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != '<media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + ' ' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap


    
