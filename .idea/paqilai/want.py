# coding=gbk
import requests  #导入requests库
import re
import pymysql
from bs4 import BeautifulSoup
#电影天堂欧美 日韩 国内  电影爬取
db = pymysql.connect(host="localhost",user="root",password="123456",db="ssm_wei",port=3306)

#电影 详情页的的基本前缀

site = 'http://www.ygdy8.net'

#构建电影类

class Movie:
    def __init__(self,name,translatedNames,year,area,type,link):
        self.name = name  #译名
        self.translatedNames = translatedNames #译名
        self.year = year #年代
        self.area = area #产地
        self.type = type #类别
        self.link = link #下载链接



    def __str__(self):
        return '%s,\t下载地址:%s,译名:%s,年代:%s,产地:%s,类别:%s'%(self.name, self.link,self.translatedNames,self.year,self.area,self.type)

    __repr__ = __str__


def getSoup(url):
    r = requests.get(url)
    r.encoding = 'gb2312'
    return  BeautifulSoup(r.text,"html.parser")


def findMovie(url):
    soup = getSoup(url)
    tables = soup.find_all('table', class_='tbspan')
    for table in tables:
        #传入正则表达式，查找所有的a标签文本内容中含有《的内容

        # aContent是匹配到a标签text里面包含《的整个a标签
        aContent = table.find_all('a')
        try:
            url = site + aContent[1]['href']
            #getMovieData(url)
            movie =  getMovieData(url)
            saveMovie(movie)
            print(movie)

        except:
            print('error !!')



def getMovieData(url):
    soup = getSoup(url)

    name = soup.find('h1').text
    name = re.findall('(?<=《)[^》]+(?=》)',name)[0]


    dataSpan = soup.find('span', attrs={"style": "FONT-SIZE: 12px"})
    dataP = dataSpan.find('p')
    dataBrs = dataP.text.replace('<br>','')
    dataBrs = dataBrs.replace('\u3000\u3000','')
    dataBrs = dataBrs.replace(' ','')
    data = dataBrs.split('◎')
    #译名
    translatedNames = data[1][3:]
    #年代
    year = data[3][3:]
    #产地
    area = data[4][3:]
    #类别
    type = data[5][3:]
    #下载链接
    downloadTd = soup.find('td', attrs={"style": "WORD-WRAP: break-word"})
    downloadA = downloadTd.find('a')
    link = downloadA['href']
    #封装成movie对象
    movie = Movie(name,translatedNames,year,area,type,link)
    return movie

def saveMovie(movie):
    cur = db.cursor()
    sql = """insert into movie(name,translated_names,year,area,type,link) VALUES ('%s','%s','%s','%s','%s','%s')"""%\
          (movie.name,movie.translatedNames,movie.year,movie.area,movie.type,movie.link)
    try:
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()



if __name__ == '__main__':
    for index in range(188):
        index += 1
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_' + str(index) + '.html'
        findMovie(url)
    db.close()
