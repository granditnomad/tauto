import requests
import os
import random
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime
import datetime
import json
import xmltodict
import FinanceDataReader as fdr


today = datetime.datetime.now(timezone('Asia/Seoul'))


def getNewsFromRss():
      RSS_URL = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR'
      res = requests.get(RSS_URL)
      ordered_dict = xmltodict.parse(res.text)
      json_type = json.dumps(ordered_dict)
      res_dict = json.loads(json_type)

      itemList = res_dict['rss']['channel']['item']
      newsList = []

      for idx,item in enumerate(itemList):
            news_item_list = item['ht:news_item']

            def mapping (news_item):
                  temp_dict = dict()
                  temp_dict['title'] = news_item['ht:news_item_title']
                  temp_dict['descript'] = news_item['ht:news_item_snippet']
                  temp_dict['url'] = news_item['ht:news_item_url']
                  temp_dict['source'] = news_item['ht:news_item_source']
                  return temp_dict

            if(isinstance(news_item_list,list)):
                  for n_idx, news_item in enumerate(news_item_list):
                        newsList.append(mapping(news_item))
            else:
                  news_item = news_item_list
                  newsList.append(mapping(news_item))

      return newsList

def get_news():
      print(f'\n\n뉴스 기사 수집을 시작합니다...')
      newsList = getNewsFromRss()
      resList = []

      for n_idx in range(0, 5):
            tmpList = []
            news_item = newsList[n_idx]
            print(f'{n_idx + 1} 번째 기사')
            title = news_item["title"].replace("&#39;", "")
            title = news_item["title"].replace("&quot;", "")
            tmpList.append(title)
            tmpList.append(news_item["url"])
            resList.append(tmpList)


      msg = f'''
            <br>
            <h4><a href="{resList[0][1]}">1. {resList[0][0]}</a></h4>
            <h4><a href="{resList[1][1]}">2. {resList[1][0]}</a></h4>
            <h4><a href="{resList[2][1]}">3. {resList[2][0]}</a></h4>
            <h4><a href="{resList[3][1]}">4. {resList[3][0]}</a></h4>
            <h4><a href="{resList[4][1]}">5. {resList[4][0]}</a></h4>
      '''

      return msg
      

def get_exchange_info():

      date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
      
      usd = fdr.DataReader('USD/KRW', date)
      cny = fdr.DataReader('CNY/KRW', date)
      jpy = fdr.DataReader('JPY/KRW', date)

      start_usd = usd['Open'].values[0]
      start_cny = cny['Open'].values[0]
      start_jpy = jpy['Open'].values[0]

      end_usd = usd['Close'].values[0]
      end_cny = cny['Close'].values[0]
      end_jpy = jpy['Open'].values[0]

      diff_usd = usd['Change'].values[0]
      diff_cny = cny['Change'].values[0]
      diff_jpy = jpy['Change'].values[0]

      msg = f'''
            <p> <b>달러(USD)</b> 환율 변동 {diff_usd} </p>
            <p> 시가 : {start_usd} / 종가 : {end_usd} </p>
            <br>
            <p> <b>위안화(CNY)</b> 환율 변동 {diff_cny} </p>
            <p> 시가 : {start_cny} / 종가 : {end_cny} </p>
            <br>
            <p> <b>엔화(JPY)</b> 환율 변동 {diff_jpy} </p>
            <p> 시가 : {start_jpy} / 종가 : {end_jpy} </p>
            <br>
      '''

      return msg


def get_random_img():
      client_key = '736-WC09y7Igc5nZBQJeIPIKBsZadWszwGyhb_w740w'
      URL = 'https://api.unsplash.com/photos/random?client_id='+client_key 

      headers = {'Authorization': client_key}
      params = {'query': 'flower', 'count': '2'}

      res = requests.get(URL, headers=headers, params=params)
      result = json.loads(res.text)

      img1 = result[0]['urls']['small']
      img2 = result[1]['urls']['small']

      return img1, img2

def make_post():
      date1 = today.strftime('%Y-%m-%d')
      date2 = today.strftime('%Y년 %m월 %d일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')


      img1, img2 = get_random_img()

      title = date1 + " 오늘의 세상 이야기"

      emoji = ["☺","😀","😄","🤩","😎","😆","😄","👍"]
      random_pick1 = emoji[random.randint(0, len(emoji)-1)]
      random_pick2 = emoji[random.randint(0, len(emoji)-1)]
      content = f'''
      
      <p> <img src="{img1}"/> </p>
      <br><br>
      <p> 안녕하세요 독자 여러분들! {random_pick1}</p>
      <p> 오늘의 날짜는 {date2} 입니다. </p> 
      <p> 어김없이 따끈따끈한 소식을 들고 찾아왔습니다 {random_pick2} </p>
      <p> 세상 살아가는 이야기, 오늘의 핫이슈와 국제 환율 정보를 알아보도록 하겠습니다! </p>
      
      <hr />

      <h3> 오늘의 주요 뉴스 top5 </h3>
      <p>{get_news()}</p>
      <br><br>
      <hr />

      <h3> 오늘의 환율 정보 </h3>
      <br>
      <p>{get_exchange_info()}</p>
      <br><br>
      <hr>
      <br>
      <p> <img src="{img2}"/> </p>
      <br>
      <p> 오늘 하루도 고생 많으셨습니다.</p>
      <p> 우리 모두 내일도 화이팅 합시다! </p>
      <br><br>
      <p> 이 포스팅은 python 자동포스팅 프로그램을 통해 작성된 글입니다! {random_pick1}</p> 
      '''

      return title, content



def post_tistory():
     tistory_url = 'https://www.tistory.com/apis/post/write?'
     
     title, content = make_post()

     data = {
           'access_token': '0ff07acfacc92a82f2e789b6a0836ba7_c038e8b7bc7e084d50e9f1d4cd3a3b6f',
           'output': '{output-type}',
           'blogName': 'grandit',
           'title': title,
           'content': content,
           'visibility': '3',
           'category': '0',
           'tag': ',',
           'acceptComment': '1'
     }
     result = requests.post(tistory_url, data=data)
     result = BeautifulSoup(result.text)
     print(result.prettify())

post_tistory()
