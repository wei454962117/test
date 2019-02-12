# -*- encoding:utf-8 -*-
import requests  #导入requests库11111111
import re
import pymysql
from bs4 import BeautifulSoup

#链接数据库
db = pymysql.connect(host="localhost",user="root",password="123456",db="ssm_wei",port=3306)

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}


def getMovieData(url):
    res = requests.get(url,allow_redirects=False,headers = header).content.decode('utf-8')
    res = BeautifulSoup(res,"html.parser")
    searchList = res.find('dd')
    searchUrl = searchList.find('a')['href']

    res2 = requests.get(searchUrl,headers = header).content.decode('utf-8')
    res2 = BeautifulSoup(res2,"html.parser")
    res3 = res2.find('div', class_='lemma-summary')

if __name__ == '__main__':
    url = "https://baike.baidu.com/search?pn=0&rn=0&enc=utf8&word=超凡蜘蛛侠/蜘蛛侠4"
    res = requests.get(url,allow_redirects=False,headers = header).content.decode('utf-8')
    #res.encoding = 'utf-8'
    res = BeautifulSoup(res,"html.parser")
    print("-----------------------")
    searchList = res.find('dd')
    searchUrl = searchList.find('a')['href']
    print(searchUrl)
    print("-----------------------")
    res2 = requests.get(searchUrl,headers = header).content.decode('utf-8')
    res2 = BeautifulSoup(res2,"html.parser")

    res3 = res2.find('div', class_='lemma-summary')
    print(res3.text)


    print("-----------------------")


    res4 = res2.find('div',class_='basic-info cmn-clearfix')
    res4Key = res4.find_all('dt')
    for i in res4Key:
        i = i.text.split('\xa0')
    res4Value = res4.find_all('dd')
    dict={}

    for i in range(len(res4Key)):
        dict[res4Key[i].text]=res4Value[i].text.strip()
    print(dict)










