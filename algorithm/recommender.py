#!/usr/bin/env python
# coding: utf-8

# # Content-based Filtering Recommendation
# Choose playlist

# In[25]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import re
import requests, json


# In[26]:


# load prepared data
playlistDF = pd.read_csv("processed_data.csv")
songDF = pd.read_csv("allsong_data.csv")
complete_feature_set = pd.read_csv("complete_feature.csv")


# In[27]:


# get playlist info from frontend
print("getting playlist info...")

# JSON file
f = open ('playlist.json', "r")
  
# Reading from file
data = json.loads(f.read())

# url = requests.get("https://project1-b1937-default-rtdb.firebaseio.com/users.json")
# text = url.text
# data = json.loads(text)
#print(data)
playlist_raw = data['items']
#print(c)
# uid = data['user']
# print(uid)

playlistDF_test = pd.DataFrame(columns = list(playlistDF.columns))

# for i in range(5):
#     print(playlistDF.loc[i]["track_uri"])
for i in range(len(songDF)):
    for j in range(len(playlist_raw)):
        if songDF.loc[i]["id"] == playlist_raw[j]:
            #print("here")
            playlistDF_test = playlistDF_test.append(playlistDF.loc[i])
            #print(playlistDF_test)
            break

playlistDF_test
print("playlist info loaded successfully.")


# In[28]:


def generate_playlist_feature(complete_feature_set, playlist_df):
    '''
    Summarize a user's playlist into a single vector
    ---
    Input: 
    complete_feature_set (pandas dataframe): Dataframe which includes all of the features for the spotify songs
    playlist_df (pandas dataframe): playlist dataframe
        
    Output: 
    complete_feature_set_playlist_final (pandas series): single vector feature that summarizes the playlist
    complete_feature_set_nonplaylist (pandas dataframe): 
    '''
    
    # Find song features in the playlist
    complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
    # Find all non-playlist song features
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]
    complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns = "id")
    return complete_feature_set_playlist_final.sum(axis = 0), complete_feature_set_nonplaylist


# In[29]:


# Generate the features
print("generating features...")
complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(complete_feature_set, playlistDF_test)


# In[30]:


# Non-playlist features
complete_feature_set_nonplaylist = complete_feature_set_nonplaylist.head(-28000)


# In[31]:


# Summarized playlist features
#complete_feature_set_playlist_vector


# In[32]:


def generate_playlist_recos(df, features, nonplaylist_features):
    '''
    Generated recommendation based on songs in aspecific playlist.
    ---
    Input: 
    df (pandas dataframe): spotify dataframe
    features (pandas series): summarized playlist feature (single vector)
    nonplaylist_features (pandas dataframe): feature set of songs that are not in the selected playlist
        
    Output: 
    non_playlist_df_top_40: Top 40 recommendations for that playlist
    '''
    
    non_playlist_df = df[df['id'].isin(nonplaylist_features['id'].values)]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis = 1).values, features.values.reshape(1, -1))[:,0]
    non_playlist_df_top_20 = non_playlist_df.sort_values('sim',ascending = False).head(20)
    
    return non_playlist_df_top_20


# In[33]:


# Genreate top 10 recommendation
print("generating playlist recommendation...")
recommend = generate_playlist_recos(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)
recommend = recommend[['id','artist_name', 'track_name']].reset_index(drop=True)
#recommend
print("recommendation generated successfully.")


# In[34]:


# recommend_dict = recommend.to_dict(orient='records')
recommend_dict = recommend['id'].to_dict()
# recommend_dict


# In[35]:


data.update({data['user']:[recommend_dict]})
json.dump(data, "recommendation.json")


# In[36]:


#requests.post("https://project1-b1937-default-rtdb.firebaseio.com/users.json", json=recommend_dict)


# In[ ]:




