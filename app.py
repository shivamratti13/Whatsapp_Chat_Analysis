import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages,words,media_shared,links_shared = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Words")
            st.title(words)

        with col2:
            st.header("Total Messages")
            st.title(num_messages)

        with col3:
            st.header("Media Shared")
            st.title(media_shared)

        with col4:
            st.header("Total URL's")
            st.title(links_shared)

    #monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color = 'pink')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

    # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messages'],color = 'brown')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

    # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


    # finding the bussiest user in the group
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = helper.fetch_most_active_users(df)
            fig, ax = plt.subplots()
            
            col5,col6 = st.columns(2)

            with col5:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col6:
                st.dataframe(new_df)

    # wordcloud
        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

    #most Commom Words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user,df)
        
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        
        st.pyplot(fig)

    # emoji
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        if emoji_df.empty:
            st.write("No emojis used.")
        else:

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)