import requests
import json

def create_url(ids_list):
    query = " OR ".join([f"from:{user}" for user in ids_list])
    tweet_fields = "tweet.fields=author_id,text"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}&expansions=author_id"
    return url

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def create_links() :
    with open("twitterAPI/infos.json") as infos:
        infos = json.load(infos)

    previous_tweets = infos["tweet_ids"]
    bearer_token = infos["token"]
    ids = infos["user_ids"]
    
    url = create_url(ids)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = connect_to_endpoint(url, headers)
    
    users = {user["id"] : user["name"] for user in response["includes"]["users"]}
    tweets = []
    for tweet in response["data"] :
        if tweet["id"] not in previous_tweets :
            link = f"https://twitter.com/{tweet['author_id']}/status/{tweet['id']}"
            tweets.append(
                {
                    "user": users[tweet['author_id']], 
                    "link": link, 
                    "tweet_id": tweet['id']}
                )
            previous_tweets.append(tweet["id"])
    
    infos["tweet_ids"] = previous_tweets
    with open("twitterAPI/infos.json", "w+") as fp :
        fp.write(json.dumps(infos, indent=2))
    
    return tweets

if __name__ == "__main__":
    print(create_links())
