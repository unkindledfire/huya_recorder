import base64
import hashlib
import re
import time
from urllib import parse

import urllib3


class HUYA:
    def __init__(self, url):
        self.__url = url

    @staticmethod
    def huya_parse(url):
        a, b = url.split("?")
        r = a.split("/")
        r_m3u8 = re.sub(r".(flv|m3u8)", "", r[-1])
        c = [i for i in b.split('&', 3) if i != '']
        # print(c)
        d = {a.split('=')[0]: a.split('=')[1] for a in c}
        e = parse.unquote(d["fm"])
        f = base64.b64decode(e).decode("utf-8").split("_")[0]
        g = str(int(time.time() * 1e7))
        h = d["wsTime"]
        l = "0"
        m = hashlib.md5("_".join([f, l, r_m3u8, g, h]).encode("utf-8")).hexdigest()
        n = c[-1]
        return f"{a}?wsSecret={m}&wsTime={h}&u={l}&seqid={g}&{n}"

    def fetch_m3u8(self):
        try:
            pm = urllib3.PoolManager()
            roompage_url = "https://m.huya.com/" + self.__url
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/79.0.3945.88 Mobile Safari/537.36'
            }
            res = pm.request("GET", roompage_url, headers=headers).data.decode("utf-8")
            live_url = re.search(r'var liveLineUrl = "(.*)";', res).group(1)
            if live_url is not None:
                if 'replay' in live_url:
                    r_url = {"replay": "https:" + live_url}
                else:
                    a_url = self.huya_parse(live_url)
                    b_url = self.huya_parse(live_url.replace("_2000", ""))
                    r_url = {
                        "2000p": "https:" + a_url,
                        "tx": "https:" + b_url,
                        "bd": "https:" + b_url.replace("tx.hls.huya.com", "bd.hls.huya.com"),
                        "migu-bd": "https:" + b_url.replace("tx.hls.huya.com", "migu-bd.hls.huya.com")
                    }
            else:
                raise Exception("找不到在线状态")
        except Exception as e:
            print(e)
            return False
        return r_url["migu-bd"]


'''def get_url(room):
    try:
        getm3u8 = HUYA(room)
        return getm3u8.fetch_m3u8()
    except Exception as e:
        print(e)
        print("get_url")
        return False'''
