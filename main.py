from TikTokApi import TikTokApi
import sys
from selenium import webdriver
from modules import *

verifyFp = "verify_kpns7g07_Xtw0Ebms_DIxR_4qO9_Afxk_jCeZkNj4CaW4"
api = TikTokApi(use_selenium=True, use_test_points=True)
data_path = str(sys.argv[1])

# get video url
urls = get_links(data_path)
print(data_path)

# get video id
video_id_list = []
for url in urls:
    try:
        # print(expand_short_url(url)) # debug
        video_id_list.append(expand_short_url(url).split("/video/")[1].split("?")[0])
    except:
        print("Link is invalid")
    # if len(video_id_list) > 50:
    #     break

full_video_data = []

for v_id in video_id_list:
    video_data = api.getTikTokById(v_id, custom_verifyFp=verifyFp)
    try:
        video_data = gather_data(video_data)

        if video_data["username"] == '':
            video_data["username"] = "访问问不了"

        print(video_data)
        # debug
        # json_obj = json.dumps(video_data, indent=4)
        # print(json_obj)
    except:
        print(sys.exc_info()[0])
        print("视频数据有问题")

    full_video_data.append(video_data)

data_df = pd.DataFrame(full_video_data)
data_path = data_path.split("/")[-1]
print(data_path)

data_df.to_csv(f"./results/{data_path}", index=False)
print("Done...")
