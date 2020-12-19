import asyncio
import re
import threading
import time

from aiohttp import ClientSession

from dm_core.utils import ListenClient
from get_m3u8.fetch_flv import ensure_ok
from get_m3u8.fetch_flv import flv_fetch
from get_m3u8.get_r_url import HUYA
from get_m3u8.fetch_flv import ensure_ok


def run_m3u8(url):
    while ensure_ok(url) == 0:
        time.sleep(1)
    r_url = HUYA(url).fetch_m3u8()
    flv_fetch(r_url)

async def star_conn(room):
    url = f'https://m.huya.com/{room}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Mobile Safari/537.36'
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            page_content = await res.text()
            if re.search(r'ISLIVE = true', page_content, re.MULTILINE) is not None:
                return 1
    return 0


'''async def dm_print(pak):
    while True:
        p = await pak.get()
        if p['pak_type'] == "normal_dm":
            print(f'{p["time"]} {p["username"]}:{p["text"]}')'''


async def recorder(url):
    while await star_conn(url) == 0:
        time.sleep(1)
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} 该主播未上线')
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} 该主播已上线')
    # real_url = "https://www.huya.com"+url
    pak = asyncio.Queue()
    # print(url)
    cli = ListenClient(url, pak)
    # asyncio.create_task(dm_print(pak))
    await cli.link_start()


def run_recorder(url):
    asyncio.run(recorder(url))


room = input("直播间地址(复制地址栏)：\n")
url = re.findall(r".com/(.*)\?(.*)", room)[0][0] if re.search(r".com/(.*)\?", room) is not None else re.search(
    r".com/(.*)", room).group(1)
t1 = threading.Thread(target=run_m3u8, args=(url,))
t2 = threading.Thread(target=run_recorder, args=(url,))
t1.start()
t2.start()
