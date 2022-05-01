import data_cleanser as ds
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

def get_max_id_val(file_name):
    max_id=0
    try:
        read_file=open(file_name,'r', encoding="utf-8")
        header=read_file.readline()
        for i in read_file.readlines():
            data=i.split('\t')
            tweet_id = int(data[1])
            if tweet_id > max_id:
                max_id=tweet_id

        read_file.close()
    except FileNotFoundError:
            {
                print("No File")
            }
    return(max_id)

def get_min_id_val(file_name):
    min_id=0
    try:
        read_file=open(file_name,'r', encoding="utf-8")
        header=read_file.readline()
        for i in read_file.readlines():
            data=i.split('\t')
            tweet_id = int(data[1])
            if tweet_id > min_id:
                min_id=tweet_id

        read_file.close()
    except FileNotFoundError:
            {
                print("No File")
            }
    return(min_id)

def get_data_string(data):
    columns= ['created_at', 'id', 'text', 'truncated', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive', 'lang']
    users = ['id','name','screen_name','location','url','followers_count','friends_count','favourites_count','utc_offset','time_zone']
    str_dat=""
    for i in columns:
        if i in data.keys():
            dat=data[i]
            if i == 'text':
                dat = str(dat)
                dat=dat.replace("\t", " ")
                dat=dat.replace("\n", ".")
        else:
            dat=""
        #print(dat)
        str_dat=str_dat+f"{dat}"+"\t"
    for j in users:
        if j in data['user'].keys():
            dat=data['user'][j]
        else:
            dat=""
        str_dat=str_dat+f"{dat}"+"\t"
    return(str_dat)

def stringify_data(data):
    dat = str(data)
    dat=dat.replace("\t", " ")
    dat=dat.replace("\n", ".")
    return dat


def write_to_file(api,tweets,file_name):
    write_header(file_name)
    write_file = open(file_name, "a", encoding="utf-8")
    for i in tweets:
        dat = get_data_string(i._json)
        status = api.get_status(i._json['id'], tweet_mode="extended")
        try:
            tweet_text = status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            tweet_text = status.full_text
        dat += stringify_data(tweet_text)
        write_file.write(dat + "\n")
    write_file.close()

def write_header(file_name):
    header = ['created_at', 'id', 'text', 'truncated', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
              'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'geo', 'coordinates',
              'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted',
              'possibly_sensitive', 'lang', 'User_id', 'User_name', 'User_screen_name', 'User_location', 'User_url',
              'User_followers_count', 'User_friends_count', 'User_favourites_count', 'User_utc_offset', 'time_zone','Tweet_data']
    dat = ""
    for i in header:
        dat += i + "\t"
    write_file = open(file_name, "w", encoding="utf-8")
    write_file.write(dat + "\n")
    write_file.close()

def clean_tweets(data):
    data['clean_tweet'] = data['Tweet_data'].apply(lambda x: ds.data_digest(x))
    return data

def annotate_tweets(data):
    data['sentiment'] = data['Tweet_data'].apply(lambda x: sentiment_scores(x))
    return data

def load_dataFrame(file_name):
    File = file_name
    low_memory = False
    data = pd.read_csv(File, sep='\t')
    data = clean_tweets(data)
    data = annotate_tweets(data)
    data = append_states(data)
    return data

def sentiment_scores(sentence):
    sentiment=None
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
#     print("Overall sentiment dictionary is : ", sentiment_dict)
#     print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
#     print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
#     print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
#     print("Sentence Overall Rated As", end = " ")
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        sentiment="Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        sentiment="Negative"
    else :
        sentiment="Neutral"
    return sentiment

def load_states():
    name = "united_states_code.txt"
    USA_Codes = pd.read_csv(name, sep='\t')
    return USA_Codes

def random_distribute_state(x):
    data=load_states()
    n = random.randint(x,x+10)
    state= data['State'][n]
    code= data['Postal'][n]
    return  pd.Series([state,code])

def append_states(data):
    input = random.randint(0, 42)
    data[['state_name','state']] = data.apply(lambda x: random_distribute_state(input), axis=1)
    return data