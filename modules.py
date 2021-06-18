import time, json, requests, sys, csv
import pandas as pd

# convert timestamp to human readable date format
def timestamp_to_humandate(timestamp):
    date = time.strftime("%Y-%m-%d", time.localtime(timestamp))
    return date

# expand shortened url (in this case TikTok's shortened url)
def expand_short_url(short_url):
    response = requests.get(short_url)
    full_url = response.url
    return full_url.split("/?")[0]

# gather required data
def gather_data(tiktok_dict):
    user_data = {}
    try:
        tiktok_data = tiktok_dict["itemInfo"]["itemStruct"]
        # user info
        user_data['username'] = tiktok_data['author']['uniqueId']
        user_data['followers'] = tiktok_data['authorStats']["followerCount"]

        # video information
        user_data['createTime'] = timestamp_to_humandate(tiktok_data['createTime'])
        user_data['videoDesc'] = tiktok_data["desc"]
        user_data['videoID'] = tiktok_data['id']
        user_data['videoLink'] = "https://www.tiktok.com/@{}/video/{}?lang=en".format(user_data['username'], user_data['videoID'])

        # video stats
        user_data['nViews'] = tiktok_data['stats']['playCount']
        user_data['nShare'] = tiktok_data['stats']['shareCount']
        user_data['nLikes'] = tiktok_data['stats']['diggCount']
        user_data['nComment'] = tiktok_data['stats']['commentCount']
        user_data["hashtag"] = [tiktok_data["challenges"][i]["title"] for i in range(len(tiktok_data["challenges"]))]
    except:
        pass

    return user_data

# get video links
def get_links(fpath):
    df = pd.read_csv(fpath)
    return df["link video"].values.tolist()
