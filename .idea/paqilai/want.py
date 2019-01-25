# coding=gbk
import requests  #导入requests库
import re
import pymysql
from bs4 import BeautifulSoup
#电影天堂欧美 日韩 国内  电影爬取
db = pymysql.connect(host="localhost",user="root",password="123456",db="ssm_wei",port=3306)

#电影 详情页的的基本前缀

site = 'https://www.dytt8.net'

#构建电影类

class Movie:
    def __init__(self,name,translatedNames,year,area,type,link,IMDbPoint,douPoint,time,language,releaseTime):
        self.name = name  #名字
        self.translatedNames = translatedNames #译名
        self.year = year #年代
        self.area = area #产地
        self.type = type #类别
        self.link = link #下载链接
        self.IMDbPoint = IMDbPoint #IMDb评分
        self.douPoint = douPoint #豆瓣评分
        self.time = time #片长
        self.language = language #语言
        self.releaseTime = releaseTime #上映时间



    def __str__(self):
        return '%s,\t下载地址:%s,译名:%s,年代:%s,产地:%s,类别:%s,IMDb评分:%s,豆瓣评分:%s,片长:%s,语言:%s,上映时间:%s'%(self.name, self.link,self.translatedNames,self.year,self.area,self.type,self.IMDbPoint,self.douPoint,self.time,self.language,self.releaseTime)

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
    #dataP = dataSpan.find('p')
    dataBrs = dataSpan.text.replace('<br>','')
    dataBrs = dataBrs.replace('\u3000\u3000','')
    dataBrs = dataBrs.replace(' ','')
    data = dataBrs.split('◎')
    print(data)
    #将数据存进字典里，和java 的map差不多
    dict={}
    for i in range(1, len(data)-2):
        dataChild = data[i].split('\u3000')
        if(len(dataChild) == 2):
            dict[dataChild[0]]=dataChild[1]

    #译名
    translatedNames = dict.get('译名')
    #年代
    year = dict.get('年代')
    #产地
    area = dict.get('国家')
    #类别
    type = dict.get('类别')
    #IMDb评分
    IMDbPoint = dict.get('IMDb评分')
    #豆瓣评分
    douPoint = dict.get('豆瓣评分')
    #片长
    time = dict.get('片长')
    #语言
    language = dict.get('语言')
    #上映时间
    releaseTime = dict.get('上映日期')
    #下载链接
    downloadTd = soup.find('td', attrs={"style": "WORD-WRAP: break-word"})
    downloadA = downloadTd.find('a')
    link = downloadA['href']
    #封装成movie对象
    movie = Movie(name,translatedNames,year,area,type,link,IMDbPoint,douPoint,time,language,releaseTime)
    return movie

def saveMovie(movie):
    cur = db.cursor()
    sql = """insert into movie(name,translated_names,year,area,type,link,IMDb_point,dou_point,time,language,releaseTime,catagory) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',2)"""%\
          (movie.name,movie.translatedNames,movie.year,movie.area,movie.type,movie.link,movie.IMDbPoint,movie.douPoint,movie.time,movie.language,movie.releaseTime)
    try:
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()



if __name__ == '__main__':
    for index in range(2):
        index += 112
        print(index)
        url = 'https://www.dytt8.net/html/gndy/china/list_4_' + str(index) + '.html'
        findMovie(url)
    db.close()
