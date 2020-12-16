import json
import requests
from pandas.io.json import json_normalize
# 라이브러리 임포트하기
import schedule
import time
from bs4 import BeautifulSoup # html 분석 라이브러리


import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
# json_slack_path = "./token.json"
# with open(json_slack_path,'r') as json_file:
    # slack_dict = json.load(json_file)
req = requests.get("http://ncov.mohw.go.kr/")

# print(req.text)
# html 잘 받아졌는지 test 문

# html 분석법
soup = BeautifulSoup(req.text,"html.parser")
# 앞에 html <> 구조까지 출력된다
# print(soup)

# chrome f12 개발자모드에서 
# 일일확진자. 국내발생. 해외유입 위치 확인하기 

국내, 해외 = soup.find("div", class_="liveNum_today_new").find_all("span",class_="data")
# class 를 만들어서 ㅎㅏ는게 아니니까..
# ?

# print(국내.text, 해외.text)
# totalsum = int(국내.text) + int(해외.text)
# print(str(totalsum)) 
# 천명 넘어갈때 반점이 생겨서 더하기가 안된다 ㅅㅂ

slack_token = ['xoxb-1553133161095-1591723827072-hZp71XZedBvrtKKeGJSSbwir']
# Token 문자열 변수 만들기

ChannelName = "bot_test"

URL ='https://slack.com/api/conversations.list'
# 채널 조회 API 메소드 : conversations.list

# 파라미터(매개변수)
params = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'token': slack_token
}

# API 호출
res = requests.get(URL, params = params)

channel_list = json_normalize(res.json()['channels'])
channel_id = list(channel_list.loc[channel_list['name'] == ChannelName, 'id'])[0]

print(f"""
채널 이름: {ChannelName}
채널 id: {channel_id}
""")


# 글 내용
Text = "slack bot test"

# 채널 내 문구 조회 API 메소드: conversations.list
URL = 'https://slack.com/api/conversations.history'

# 파라미터
params = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'token': slack_token,
    'channel': channel_id
         }

# API 호출
res = requests.get(URL, params = params)    

chat_data = json_normalize(res.json()['messages'])
chat_data['text'] = chat_data['text'].apply(lambda x: x.replace("\xa0"," "))
ts = chat_data.loc[chat_data['text'] == Text, 'ts'].to_list()[0]

print(f"""
글 내용: {Text}
ts: {ts}
""")

# print("Azure Blob storage v" + __version__ + " - Python slackbot sample")
# connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# container_client = blob_service_client.get_container_client("smartwatchdata")

# blob_list = container_client.list_blobs()
# print(blob_list)
# for blob in blob_list:
#     #     print("\t" + blob.name)


# Bot으로 등록할 댓글 메시지 문구
# message = f"""
# new data upload! ^^
# """
message = f"""
오늘의 코로나 확진자 현황을 알려드립니다!

국내유입 : {국내.text}
해외유입 : {해외.text}

오늘도 건강한 하루되세요! 
"""

# 파라미터
data = {'Content-Type': 'application/x-www-form-urlencoded',
        'token': slack_token,
        'channel': channel_id, 
        'text': message,
        'reply_broadcast': 'True', 
        # 'thread_ts': ts #스레드로 남길 때 사용.
        } 

# 메시지 등록 API 메소드: chat.postMessage
URL = "https://slack.com/api/chat.postMessage"
res = requests.post(URL, data=data)


