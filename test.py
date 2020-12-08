#웹 크롤링
# requests : html 파일 가져옴 ; bs4 html 분석하기 
import requests
from bs4 import BeautifulSoup

import datetime

Now = str(datetime.datetime.now())
# str로 변환해주는 이유: 그래야 배열원소 특정 값만 확인할 수 있으니까 
print(Now)
Day = Now[:4] + Now[5:7] + Now[8:10]
print(Day)
#20201101 형식을 만들것이다 
# https://corona-live.com/city/0/


req = requests.get("http://school.cbe.go.kr/chungjuja-e/M01040504/list?ymd="+Day)
#print(req.text)
soup = BeautifulSoup(req.text,"html.parser")
#print(soup)

atag = soup.find("a",href="/chungjuja-e/M01040504/list?ymd="+Day)
# print(atag)

li = atag.find_all('li')
# print(li)

식단 = ""

for i in li:
    식단 = 식단 + i.text +"\n"
print(식단)


# 텔레그램 봇 

import telegram
token = "1476128654:AAGfPMz0iUEcBCX-E0ltFCVRIdz5_wU1e_g"
bot = telegram.Bot(token=token)
for i in bot.getUpdates():
    print(i.message)

# 저 위에서 받은 아이디를 이용해야한다 
# send_message 를 사용할 때는 지금 id값을 일일이 쳐서 나오는 것이니까

bot.send_message(1493142952,"안녕하세요")