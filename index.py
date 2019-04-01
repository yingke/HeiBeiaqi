#-*- coding:utf-8 -*-
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
import re
import sys

import mysqlHelp

reload(sys)
sys.setdefaultencoding('utf8')

#获取生态环境部 首页全国质量AQI 时报


def getallcity():
    url = 'http://datacenter.mee.gov.cn/aqiweb2/'
    r = requests.get(url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    tb = soup.find(id="legend_01_table").find_all("tr")
    tr = tb[0].get("onclick")
    riqi = re.findall(r"[(](.*?)[)]", tr)
    listaqi = []
    for i in tb:
        aqi = []

        riqi = re.findall(r"[(](.*?)[)]", i.get("onclick"))
        time = re.findall(r"\'(.+?)\'", riqi[0])
        aqi.append(time[1].replace('年', '-').replace('月', '-').replace('日', ' ').replace('时', ':00:00'))
        print(time[1].replace('年', '-').replace('月', '-').replace('日', ' ').replace('时', ':00:00'))
        td = i.find_all("td")
        for d in td:
            for dd in d:
                print(dd.strip())
                aqi.append(dd.strip())

        listaqi.append(tuple(aqi))



    mysqlHelp.addcrows(
        "INSERT INTO allcitys (DataTime ,CityName ,AQI ,PM25 ,PM10, SO2, NO2,CO,O3, MaxPoll  ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        listaqi)


def getday():
    url = 'http://datacenter.mee.gov.cn/aqiweb2/'
    r = requests.get(url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    tb = soup.find(id="legend_02_table").find_all("tr")

    listaqi = []
    for i in tb:
        aqi = []

        riqi = re.findall(r"[(](.*?)[)]", i.get("onclick"))
        time = re.findall(r"\'(.+?)\'", riqi[0])
        aqi.append(time[1].replace('年', '-').replace('月', '-').replace('日', ' ').replace('时', ':00:00'))
        print(time[1].replace('年', '-').replace('月', '-').replace('日', ' ').replace('时', ':00:00'))
        td = i.find_all("td")
        for d in td:
            for dd in d:
                print(dd.strip())
                aqi.append(dd.strip())

        listaqi.append(tuple(aqi))
    mysqlHelp.addcrows(
        "INSERT INTO quanguoallcitys (DataTime ,CityName ,AQI ,Type, MaxPoll  ) VALUES(%s,%s,%s,%s,%s)", listaqi)


    pass


def job():
    sched = BlockingScheduler()
    sched.add_job(getallcity, 'interval', hours=1,misfire_grace_time=300)
    sched.start()
    pass


if __name__ == '__main__':
    getallcity()
    job()
