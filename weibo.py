import requests
from bs4 import BeautifulSoup
import pandas as pd
import bs4
import json
host = 'https://s.weibo.com'
url = host + '/top/summary?cate=realtimehot'
write_url = 'http://127.0.0.1/api/articles'

def getHTMLText(url):
    try:
        kv = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53",
            # "Cookie": 'UOR=,,login.sina.com.cn; ALF=1666445729; SCF=AscEHVE2sTV05zTwYj5M7tduM7Zz3ktqPi21c2dTBB0sGFGcFIldixokcQ1yN8xFwVW-ywKnUt3rugqpWgzVXsE.; SINAGLOBAL=7267933806159.166.1634959444829; SUB=_2AkMW3d0wf8NxqwJRmPERzW_nbIx0yQ7EieKggSzrJRMxHRl-yT9jqhdftRB6PV3z3z21fp5a3CkZMXy5gZcyj15_nia0; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W56DO1wnAXX89yZnIENST5-; _s_tentry=-; Apache=6131946571247.373.1639292770571; ULV=1639292770592:2:1:1:6131946571247.373.1639292770571:1634959444907'
            'Cookie': 'SUB=_2AkMUSh1pf8NxqwJRmP8dy2rhaoV2ygrEieKiFuyyJRMxHRl-yT9jqnBYtRB6P8ozhi7WJm1lEEeoSj58W83dYs3rj12l'           
        }
        r = requests.get(url, headers=kv, timeout=30)
        #请求返回错误码时抛出 HTTPError 异常
        r.raise_for_status()
        #设置 HTTP 响应内容的编码方式为最可能的编码方式
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error"
    
def addArticles(url, json_data):   
    try:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, headers=headers, data=json_data)
        # print(r.json())

        #请求返回错误码时抛出 HTTPError 异常
        r.raise_for_status()
        #设置 HTTP 响应内容的编码方式为最可能的编码方式
        r.encoding = r.apparent_encoding
        return r
    except requests.exceptions.HTTPError as e:
        raise Exception("HTTP 请求错误：{}".format(e))
    except requests.exceptions.RequestException as e:
        raise Exception("其他请求错误：{}".format(e))

# 获取微博数据并整理    
def getWeiBoDatas(sou):
    datas = []
    count = 0
    # print(sou)
    for x in sou:
        count+=1
        td1 = x.find('td', class_='td-01')
        if td1 is not None:
        
            if td1.text.isdigit():
                td2 = x.find('td', class_='td-02')
                if td2 is not None:
                    a_tag = td2.find('a')
                    if a_tag is not None:
                        print(a_tag.get('href'), a_tag.text)
                        data = {
                            'no': td1.text,
                            'title': a_tag.string,
                            'url': a_tag.get('href'),
                            'source': 1
                        }
                        datas.append(data)
    return datas                    

html = getHTMLText(url)
soup = BeautifulSoup(html, 'html.parser')
sou = soup.find_all("tr") 
datas = getWeiBoDatas(sou)
postdata = {'data':datas}
json_data = json.dumps(postdata)

try:
    r = addArticles(write_url, json_data);
except Exception as  e:
    print("网络请求异常：{}".format(e))

 