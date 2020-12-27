import requests
import urllib3
import time
import smtplib
import email
import re
import configparser
import yaml

pm = urllib3.PoolManager()
roompage = "https://m.huya.com/"
headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/79.0.3945.88 Mobile Safari/537.36'
}
cfg = configparser.ConfigParser()
cfg.read("./config.ini")
def check(id,val):
    live = 0
    rpage = roompage+id
    while True:
        res = pm.request("GET", rpage, headers=headers).data.decode("utf-8")
        #print(res)
        live_status = re.search(r'ISLIVE = true', res, re.MULTILINE)
        if live_status is not None:
            if live == 0:
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} 该主播已上线')
                list = cfg.options("Host")
                author = re.search(r'var ANTHOR_NICK = "(.*)";', res, re.MULTILINE)
                if author is not None:
                    au = author.group(1)
                    if au not in list:
                        cfg.set("Host",id,au)
                        cfg.write(open('config.ini', "r+", encoding="utf-8"))
            live = 1
            pass
        else:
            live = 0
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} 该主播已下线')
            time.sleep(val)


interval = int(cfg.get("Default", "interval"))
roomid = cfg.get("Default","room_id")
check(roomid,interval)
