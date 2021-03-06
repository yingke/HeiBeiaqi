import xml.etree.ElementTree as ET
import datetime

import index
import mysqlHelp
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import random
from random import choice
import logging
logging.basicConfig()
uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
]

headerss = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN',
    'Connection': 'close',
    'Host': '121.28.49.85:8080',
    'Referer': 'http://121.28.49.85:8080/flash/AmsPublicClient.swf',
    'User-Agent': choice(uas),
    'x-flash-version': '32,0,0,101'
}


def getaqi():
    aqiurl='http://121.28.49.85:8080/datas/hour/130000.xml?radn=%f'%(random.random())
    r = requests.get(url=aqiurl, headers= headerss)
    parsexml(r.text)

def parsexml(xml):
    root = root = ET.fromstring(xml.encode('utf-8'))
    # tree = ET.parse('130000.xml')
    # root =  tree.getroot()
    listaqi = []
    for childs in root.findall('Citys'):
        for city in childs:
            Name = city.find('Name').text
            DataTime = (('%d' + '-' + city.find('DataTime').text) % datetime.datetime.now().year).replace('/', '-')
            AQI = city.find('AQI').text
            Level = city.find('Level').text
            Type = city.find('Type').text
            LevelIndex = city.find('LevelIndex').text
            MaxPoll = city.find('MaxPoll').text
            Intro = city.find('Intro').text
            Tips = city.find('Tips').text
            pp = city.find('Polls')
            p = getpoll(pp)
            PM25 = p['Pm25']
            PM10 = p['PM10']
            SO2 = p['SO2']
            CO = p['CO']
            NO2 = p['NO2']
            O38H = p['O3-8H']
            O31H = p['O3-1H']
            sql = (Name, DataTime, AQI, Level, Type, LevelIndex, MaxPoll, Intro, Tips,
                   PM25, PM10, SO2, CO, NO2, O38H, O31H)
            str = "INSERT INTO Citys (CityName ,DataTime ,AQI ,Level ,Type ,LevelIndex ,MaxPoll ,Intro ,Tips,PM25 , PM10 , SO2, CO, NO2 , O38H ,O31H ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

            mysqlHelp.addcrow(str, sql)
            print("Citys -->"+Name+DataTime)

            getarea(city.find('Pointers'))


def getpoll(polllist):
    global polls
    polls = {}
    for poll in polllist:
        name = poll.find('Name').text
        if 'PM2.5' in name:
            name = 'Pm25'
        poll1 = {name : poll.find('Value').text}
        polls.update(poll1)
    return polls


def getarea(Pointerlist):
    listRegionaqi = []
    for point in Pointerlist:
        City = point.find('City').text
        Region = point.find('Region').text
        Name = point.find('Name').text
        DataTime = (('%d' + '-' + point.find('DataTime').text) % datetime.datetime.now().year).replace('/', '-')
        AQI = point.find('AQI').text
        Level = point.find('Level').text
        LevelIndex = point.find('LevelIndex').text
        MaxPoll = point.find('MaxPoll').text
        Intro = point.find('Intro').text
        Tips = point.find('Tips').text
        CLng = point.find('CLng').text
        CLat = point.find('CLat').text
        p=getpoll(point.find('Polls'))
        PM25 = p['Pm25']
        PM10 = p['PM10']
        SO2 = p['SO2']
        CO = p['CO']
        NO2 = p['NO2']
        O38H = p['O3-8H']
        O31H = p['O3-1H']
        sql = (City, Region, Name, DataTime, AQI, Level, LevelIndex, MaxPoll, Intro, Tips, CLng, CLat, PM25, PM10, SO2, CO, NO2, O38H, O31H )
        listRegionaqi.append(sql)
        # str =  "INSERT INTO Region (CityName ,Region,Site,DataTime ,AQI ,Level ,LevelIndex ,MaxPoll ,Intro ,Tips, CLng,CLat,PM25 , PM10 , SO2, CO, NO2 , O38H ,O31H ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        # mysqlHelp.addcrow(str, sql)
    str =  "INSERT INTO Region (CityName ,Region,Site,DataTime ,AQI ,Level ,LevelIndex ,MaxPoll ,Intro ,Tips, CLng,CLat,PM25 , PM10 , SO2, CO, NO2 , O38H ,O31H ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    mysqlHelp.addcrows(str, listRegionaqi)


def job():
    sched = BlockingScheduler()
    sched.add_job(getaqi, 'interval', hours=1, misfire_grace_time=300)
    sched.start()
    pass



if __name__ == "__main__":
    getaqi()
    job()
    pass
