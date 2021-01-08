import os
import uuid
import re
import time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import datetime
import json 
import pandas as pd
from pandas import json_normalize
import requests

# Token 문자열 변수 만들기
# slack_token = ['xoxb-1616926072624-1578347075031-3UyDm9PYOoZnPoPB8yq42eJV']

# 채널 조회 API 메소드 : conversations.list
ChannelName = "bot_test"
URL ='https://slack.com/api/conversations.list'

# 파라미터(매개변수)
params = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'token': slack_token
}

# API 호출
res = requests.get(URL, params = params)
# channel_list = json_normalize(res.json()['channels'])
# channel_id = list(channel_list.loc[channel_list['name'] == ChannelName, 'id'])[0]

# print(f"""
# 채널 이름: {ChannelName}
# 채널 id: {channel_id}
# """)

# 환경변수 연결
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# 환경변수 출력
print(connect_str)

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# Instantiate a ContainerClient
container_client = blob_service_client.get_container_client("smartwatchdata")
blobs_filename_list = container_client.list_blobs()


# print(blobs_filename_list)
now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')
# print(now)          # 2018-07-28 12:11:32.669083
# print(nowDate)      # 2018-07-28.

new_blob = list()
post_num = 0

while True:


    for blob_filename in blobs_filename_list:
        if re.match(nowDate, blob_filename.name):
            new_blob.append(blob_filename.name)

    print(new_blob)

    if(post_num != len(new_blob)):

        late_num = int(len(new_blob))

        for i in range(post_num,late_num):
            
            message = f"""
            New file upload :
            """ + new_blob[i]
            
            print("Update File : " + new_blob[i])

            data = {'Content-Type': 'application/x-www-form-urlencoded',
            'token': slack_token,'channel': channel_id, 
            'text': message,'reply_broadcast': 'True', } 
            URL = "https://slack.com/api/chat.postMessage"
            res = requests.post(URL, data=data)

        post_num = len(new_blob)




    time.sleep(100)