
from packages.config import bearer_token1,bearer_token2,bearer_token3,bearer_token4, max_result
import requests

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token1}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']['id']

def get_user_tweets(user_id,bearer_tokens, max_results=max_result):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    print(url)
    headers = {"Authorization": f"Bearer {bearer_tokens}"}
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,text"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def hash_trend():
    # user_id = get_user_id(username)
        
    # ids={bearer_token1:'1802642686710837249',bearer_token2:'1852674305517342720',bearer_token3:'1876696076499222528',bearer_token4:'1856925315286601728'}
    ids={bearer_token3:'1876696076499222528',bearer_token4:'1856925315286601728'}
    # ids={bearer_token1:'1802642686710837249',bearer_token2:'1852674305517342720'}
    tweets_str=''

    for bearer_token, user_id in ids.items():
        bearer_token = str(bearer_token)
        user_id = str(user_id)
        try:
            print(f"Fetching tweets for user: {user_id} with token: {bearer_token}\n\n")
            tweets = get_user_tweets(user_id, bearer_token)
            print('tweets===================',tweets)
            for tweet in tweets['data']:
                tweet_text = tweet['text']
                tweets_str = tweets_str+ str(tweet['created_at']) +' '+str(tweet_text)
            print('==================================',tweets_str)
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            continue
    return tweets_str
