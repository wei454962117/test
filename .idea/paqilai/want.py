# coding=gbk
import requests  #����requests��
import re
import pymysql
from bs4 import BeautifulSoup
#��Ӱ����ŷ�� �պ� ����  ��Ӱ��ȡ
db = pymysql.connect(host="localhost",user="root",password="123456",db="ssm_wei",port=3306)

#��Ӱ ����ҳ�ĵĻ���ǰ׺

site = 'https://www.dytt8.net'

#������Ӱ��

class Movie:
    def __init__(self,name,translatedNames,year,area,type,link,IMDbPoint,douPoint,time,language,releaseTime):
        self.name = name  #����
        self.translatedNames = translatedNames #����
        self.year = year #���
        self.area = area #����
        self.type = type #���
        self.link = link #��������
        self.IMDbPoint = IMDbPoint #IMDb����
        self.douPoint = douPoint #��������
        self.time = time #Ƭ��
        self.language = language #����
        self.releaseTime = releaseTime #��ӳʱ��



    def __str__(self):
        return '%s,\t���ص�ַ:%s,����:%s,���:%s,����:%s,���:%s,IMDb����:%s,��������:%s,Ƭ��:%s,����:%s,��ӳʱ��:%s'%(self.name, self.link,self.translatedNames,self.year,self.area,self.type,self.IMDbPoint,self.douPoint,self.time,self.language,self.releaseTime)

    __repr__ = __str__


def getSoup(url):
    r = requests.get(url)
    r.encoding = 'gb2312'
    return  BeautifulSoup(r.text,"html.parser")


def findMovie(url):
    soup = getSoup(url)
    tables = soup.find_all('table', class_='tbspan')
    for table in tables:
        #����������ʽ���������е�a��ǩ�ı������к��С�������

        # aContent��ƥ�䵽a��ǩtext���������������a��ǩ
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
    name = re.findall('(?<=��)[^��]+(?=��)',name)[0]


    dataSpan = soup.find('span', attrs={"style": "FONT-SIZE: 12px"})
    #dataP = dataSpan.find('p')
    dataBrs = dataSpan.text.replace('<br>','')
    dataBrs = dataBrs.replace('\u3000\u3000','')
    dataBrs = dataBrs.replace(' ','')
    data = dataBrs.split('��')
    print(data)
    #�����ݴ���ֵ����java ��map���
    dict={}
    for i in range(1, len(data)-2):
        dataChild = data[i].split('\u3000')
        if(len(dataChild) == 2):
            dict[dataChild[0]]=dataChild[1]

    #����
    translatedNames = dict.get('����')
    #���
    year = dict.get('���')
    #����
    area = dict.get('����')
    #���
    type = dict.get('���')
    #IMDb����
    IMDbPoint = dict.get('IMDb����')
    #��������
    douPoint = dict.get('��������')
    #Ƭ��
    time = dict.get('Ƭ��')
    #����
    language = dict.get('����')
    #��ӳʱ��
    releaseTime = dict.get('��ӳ����')
    #��������
    downloadTd = soup.find('td', attrs={"style": "WORD-WRAP: break-word"})
    downloadA = downloadTd.find('a')
    link = downloadA['href']
    #��װ��movie����
    movie = Movie(name,translatedNames,year,area,type,link,IMDbPoint,douPoint,time,language,releaseTime)
    return movie

def saveMovie(movie):
    cur = db.cursor()
    sql = """insert into movie(name,translated_names,year,area,type,link,IMDb_point,dou_point,time,language,releaseTime,catagory) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',2)"""%\
          (movie.name,movie.translatedNames,movie.year,movie.area,movie.type,movie.link,movie.IMDbPoint,movie.douPoint,movie.time,movie.language,movie.releaseTime)
    try:
        # ִ��sql���
        cur.execute(sql)
        # �ύ�����ݿ�ִ��
        db.commit()
    except Exception as e:
        # �������������ع�
        db.rollback()



if __name__ == '__main__':
    for index in range(2):
        index += 112
        print(index)
        url = 'https://www.dytt8.net/html/gndy/china/list_4_' + str(index) + '.html'
        findMovie(url)
    db.close()
