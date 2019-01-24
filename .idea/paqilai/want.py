# coding=gbk
import requests  #����requests��
import re
import pymysql
from bs4 import BeautifulSoup
#��Ӱ����ŷ�� �պ� ����  ��Ӱ��ȡ
db = pymysql.connect(host="localhost",user="root",password="123456",db="ssm_wei",port=3306)

#��Ӱ ����ҳ�ĵĻ���ǰ׺

site = 'http://www.ygdy8.net'

#������Ӱ��

class Movie:
    def __init__(self,name,translatedNames,year,area,type,link):
        self.name = name  #����
        self.translatedNames = translatedNames #����
        self.year = year #���
        self.area = area #����
        self.type = type #���
        self.link = link #��������



    def __str__(self):
        return '%s,\t���ص�ַ:%s,����:%s,���:%s,����:%s,���:%s'%(self.name, self.link,self.translatedNames,self.year,self.area,self.type)

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
    dataP = dataSpan.find('p')
    dataBrs = dataP.text.replace('<br>','')
    dataBrs = dataBrs.replace('\u3000\u3000','')
    dataBrs = dataBrs.replace(' ','')
    data = dataBrs.split('��')
    #����
    translatedNames = data[1][3:]
    #���
    year = data[3][3:]
    #����
    area = data[4][3:]
    #���
    type = data[5][3:]
    #��������
    downloadTd = soup.find('td', attrs={"style": "WORD-WRAP: break-word"})
    downloadA = downloadTd.find('a')
    link = downloadA['href']
    #��װ��movie����
    movie = Movie(name,translatedNames,year,area,type,link)
    return movie

def saveMovie(movie):
    cur = db.cursor()
    sql = """insert into movie(name,translated_names,year,area,type,link) VALUES ('%s','%s','%s','%s','%s','%s')"""%\
          (movie.name,movie.translatedNames,movie.year,movie.area,movie.type,movie.link)
    try:
        # ִ��sql���
        cur.execute(sql)
        # �ύ�����ݿ�ִ��
        db.commit()
    except Exception as e:
        # �������������ع�
        db.rollback()



if __name__ == '__main__':
    for index in range(188):
        index += 1
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_' + str(index) + '.html'
        findMovie(url)
    db.close()
