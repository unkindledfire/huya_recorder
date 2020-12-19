import pathlib
import re
import time

import urllib3
from ffmpy3 import FFmpeg


def ensure_ok(url):
    pm = urllib3.PoolManager()
    roompage_url = "https://m.huya.com/" + url
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Mobile Safari/537.36'
    }
    res = pm.request("GET", roompage_url, headers=headers).data.decode("utf-8")
    if re.search(r'ISLIVE = true', res, re.MULTILINE) is not None:
        return 1
    return 0


def flv_fetch(id):
    path = pathlib.Path(".\视频")
    path.mkdir(exist_ok=True)
    ff = FFmpeg(
        inputs={id: None},
        outputs={f'.\\视频\\{int(time.time())}.flv': "-c:v copy -c:a aac"}
    )
    ff.run()
