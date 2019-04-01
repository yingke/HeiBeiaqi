import datetime
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import mysqlHelp

aqiurl = 'http://60.6.237.50:9000/AutoPublish/AjaxPublishHandler.ashx'
pm25params = {'pageName': 'Map', 'funcName': 'GetNodeList', 'para': 'PM25'}
so2params = {'pageName': 'Map', 'funcName': 'GetNodeList', 'para': 'SO2'}
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
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
     'Content-Length': '43',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
    'Host': '60.6.237.50:9000',
    'Referer': 'http://60.6.237.50:9000/AutoPublish/PublishMap.aspx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Cookie': 'ASP.NET_SessionId=3eaj2kwit3r30xu0sn1b4g2p'

}


def getpm25():
    rpm25 = requests.post(aqiurl, data=pm25params, headers=headerss)
    listpm25 = []
    for i in rpm25.json():
        name = i['name']
        lastDataTime = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:00:00")
        lat = i['lat']
        lng = i['lng']
        paraValue = i['paraValue']
        paraName = i['paraName']


        sql = (lastDataTime, name, paraValue, lat, lng)
        print(sql)
        listpm25.append(sql)
    mysqlHelp.addcrows( "INSERT INTO xthourmp25 (DataTime ,Name ,PM25 ,lat ,lng  ) VALUES(%s,%s,%s,%s,%s)",listpm25)

    pass

def getSO2():
    rso2 = requests.post(aqiurl, data=so2params, headers=headerss)
    listso2 = []
    for i in rso2.json():
        name = i['name']
        lastDataTime = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:00:00")
        lat = i['lat']
        lng = i['lng']
        paraValue = i['paraValue']
        paraName = i['paraName']
        if(lastDataTime ==""):
            time =""
        else:
            time = lastDataTime.replace('/', '-')
            pass
        sql = (time, name, paraValue, lat, lng)
        print(sql)
        listso2.append(sql)
    mysqlHelp.addcrows("INSERT INTO xthourmso2 (DataTime ,Name ,SO2 ,lat ,lng  ) VALUES(%s,%s,%s,%s,%s)", listso2)
    pass

def get():
    getpm25()
    getSO2()

def job():
    sched = BlockingScheduler()
    sched.add_job(get, 'interval', hours=1, misfire_grace_time=300)
    sched.start()
    pass
if __name__ == "__main__":
    get()
    job()

