import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

#upload a file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode('utf-8', errors='ignore')
    
    df = preprocessor.preprocess(data)
 


    #fetch unique users
    user_list = df['User'].unique().tolist()
    if 'System' in user_list:
        user_list.remove('System')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analusis wrt",user_list)
    
    #stats area
    if st.sidebar.button("Show Analysis"):
        
        num_messages , words , num_media_messages , num_url  = helper.Fetch_Stats(selected_user , df)
        st.title("Top Statastics")
        col1 , col2 ,col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_url)

        st.markdown("---")

    # monthly_timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user , df)
        fig , ax = plt.subplots()
        ax.plot(timeline['time'],timeline['Message'],color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.markdown("---")

    # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user , df)
        fig , ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['Message'],color = 'magenta')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.markdown("---")

    # activity map:
        st.title("Activity Map")
        col1 , col2 = st.columns(2)
    # most busy day
        with col1 : 
            st.title("Most busy day")
            weekly_activity = helper.weekly_activity_map(selected_user , df)
            fig , ax = plt.subplots()
            ax.bar(weekly_activity.index , weekly_activity.values , color = plt.cm.plasma( plt.Normalize(weekly_activity.min(), weekly_activity.max())(weekly_activity) ))
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2 : 
            st.title("Most busy month")
            month_activity = helper.monthly_activity_map(selected_user , df)
            fig , ax = plt.subplots()
            ax.bar(month_activity.index , month_activity.values , color = plt.cm.cividis_r( plt.Normalize(month_activity.min(), month_activity.max())(month_activity) ))
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        st.markdown("---")
        # activity Heatmap
        
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        st.markdown("---")


    # most busy perosns(Group Level)

        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x , new_df= helper.Most_Busy_Person(df)
            fig , ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values , color = 'red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        st.markdown("---")
        #worcloud
        st.title("WordCloud")
        df_wc = helper.create_worcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.markdown("---")

        # most used words
        most_common_words_df = helper.most_common_words(selected_user , df)

        fig , ax = plt.subplots()

        ax.barh(most_common_words_df[0] , most_common_words_df[1])
        # plt.xticks(rotation = 'vertical')
        st.title("Most common words")
        st.pyplot(fig)
        st.markdown("---")

        # emoji analysis
        st.title("Emoji Analysis")
        emoji_df , num_emoji = helper.emoji_helper(selected_user , df)

        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            top_emojis = emoji_df.head()

            fig = px.pie(
                values=top_emojis[1],
                names=top_emojis[0],
                title="Top Emojis"
            )

            st.plotly_chart(fig, use_container_width=True)

        


        

        







    





