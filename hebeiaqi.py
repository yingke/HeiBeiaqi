import xml.etree.ElementTree as ET
import datetime
from bmob import *
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import random
from random import choice
import json
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
    'Connection': 'keep-alive',
    'Host': '121.28.49.85:8080',
    'Referer': 'http://121.28.49.85:8080/flash/AmsPublicClient.swf',
    'User-Agent': choice(uas),
    'x-flash-version': '32,0,0,101'
}
aqiurl='http://121.28.49.85:8080/datas/hour/130000.xml?radn=%f'%(random.random())
appid = 'd381adaa0588345fbec65b7da695650c'
restkey = 'ca3ce7f1936e41b6f9fa79c38e666ae5'
def getaqi():
    r = requests.get(url=aqiurl, headers= headerss)

    parsexml(r.text)

def parsexml(xml):
    root = root = ET.fromstring(xml.encode('utf-8'))
    # tree = ET.parse('130000.xml')
    # root =  tree.getroot()
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
            data = {
                'Name':Name,
                'DataTime':DataTime,
                'AQI': AQI,
                'Level': Level,
                'Type': Type,
                'LevelIndex': LevelIndex,
                'MaxPoll': MaxPoll,
                'Intro': Intro,
                'Tips': Tips}
            d=dict(data.items()+getpoll(city.find('Polls')).items())
            getarea(city.find('Pointers'))

            b =Bmob(appid,restkey)
            print(b.insert('citiys',d).jsonData)

def getpoll(polllist):
    global polls
    polls = {}
    for poll in polllist:
        name = poll.find('Name').text
        if 'PM2.5' in name:
            name = 'Pm25'
        poll1 = {name: poll.find('Value').text, }
        polls.update(poll1)
    return polls

def getarea(Pointerlist):
    global Pointers
    Pointers={}
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
        Pointers={
            'City': City,
            'Region': Region,
            'Name': Name,
            'DataTime': DataTime,
            'AQI': AQI,
            'Level': Level,
            'LevelIndex': LevelIndex,
            'MaxPoll': MaxPoll,
            'Intro': Intro,
            'Tips': Tips,
            'CLng': CLng,
            'CLat': CLat
        }
        poll=getpoll(point.find('Polls'))
        Pointers = dict(Pointers.items()+poll.items())
        b = Bmob(appid, restkey)
        print(b.insert('Region', Pointers).jsonData)
    return Pointers




def job():
    sched = BlockingScheduler()
    sched.add_job(getaqi, 'interval', seconds=3600 )
    sched.start()
    pass
if __name__ == "__main__":
    getaqi()
    job()
    pass