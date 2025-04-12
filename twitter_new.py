import requests

# Replace with your Bearer Token
#bearer_token1 = 'AAAAAAAAAAAAAAAAAAAAAAE10gEAAAAA3pMA2HfKbr7BTJbmy9ouVy0W6KY%3DsUH4wi1m01vRpn3MRsX7oVqvG1XuKCW2UFwkRMPKwvquAZaRHD'




#bearer_token1 = 'AAAAAAAAAAAAAAAAAAAAAAE10gEAAAAA6RlNYT70q%2F2KzqlDBNM3XkpLiS0%3DkDxyCD6ZINl8Lbq3HcfoissHnM5YpE4rIqL5n9uYt3ahovG3Y4'
# 
bearer_token1 ='AAAAAAAAAAAAAAAAAAAAAE820gEAAAAA6Lu0XKbbaF%2BYWNJ72o0AGjnby8k%3DldwO3II4SDU6DWI7XLF1VMexlHv8Wx7ypdQdvx7pA1O6XVhaxh'

# bearer_token1 ='AAAAAAAAAAAAAAAAAAAAAMI20gEAAAAAysuDAw5CHj3IL5G5vU%2FYZb9keg8%3Daatt6jyjQngINMWKTzuFPzafb0pY5JBAmqjflYxOjOmkNv0cQu'
max_result=2
# bearer_token1 = 'AAAAAAAAAAAAAAAAAAAAANI20gEAAAAACgEEwK6BX8JO5BI3BWPCdy8e%2BGY%3DLLdIpm0pnxwpktKehi6owvkJTKcVN4mwHiYAY4LZsmTgE26Ob8'
# Set up headers for authentication



def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token1}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print('====================================================')
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()['data']['id']
        print(data)
        return data
    except requests.exceptions.HTTPError as err:
        print("HTTP error:", err)
        print("Response content:", response.text)


def get_user_tweets(user_id,bearer_tokens, max_results=max_result):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    print(url)
    headers = {"Authorization": f"Bearer {bearer_tokens}"}
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,text"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.HTTPError as err:
        print("HTTP error:", err)
        print("Response content:", response.text)

if __name__ == "__main__":
    username = "slopfather"  # Replace with any username
    try:
        user_id = get_user_id(username)
        print(user_id)
        
        ids={bearer_token1:user_id}
        tweets_str=''

        for i in ids:
            print(ids[i],i)
            tweets = get_user_tweets(ids[i],i)
            for tweet in tweets['data']:
                print(f" {tweet['created_at']}\n {tweet['text']}\n")
                tweets_str+=f" {tweet['created_at']}\n {tweet['text']}\n"
        print(tweets_str)
    except Exception as e:
        print(f"Error: {e}")

        