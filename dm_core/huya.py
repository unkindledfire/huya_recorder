import re
import time

import aiohttp
import pymongo

from .tars import tarscore

cli = pymongo.MongoClient("mongodb://localhost:27017/")
db = cli["huya_dm"]
col = db["ori_dm"]


class HUYALIVE:
    wss_url = 'wss://cdnws.api.huya.com/'
    heartbeat = b'\x00\x03\x1d\x00\x00\x69\x00\x00\x00\x69\x10\x03\x2c\x3c\x4c\x56\x08\x6f\x6e\x6c\x69\x6e\x65\x75\x69\x66\x0f\x4f\x6e\x55\x73\x65\x72\x48\x65\x61\x72\x74\x42\x65\x61\x74\x7d\x00\x00\x3c\x08\x00\x01\x06\x04\x74\x52\x65\x71\x1d\x00\x00\x2f\x0a\x0a\x0c\x16\x00\x26\x00\x36\x07\x61\x64\x72\x5f\x77\x61\x70\x46\x00\x0b\x12\x03\xae\xf0\x0f\x22\x03\xae\xf0\x0f\x3c\x42\x6d\x52\x02\x60\x5c\x60\x01\x7c\x82\x00\x0b\xb0\x1f\x9c\xac\x0b\x8c\x98\x0c\xa8\x0c'
    heartbeatInterval = 60

    @staticmethod
    async def get_ws_info(url):
        reg = []
        t_url = 'https://m.huya.com/' + re.search(r".com/(.*)", url).group(1)
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.88 Mobile Safari/537.36'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as res:
                page = await res.text()
                ayuid = re.search(r"ayyuid: +'([0-9]+)'", page, re.MULTILINE).group(1)
                tid = re.search(r"TOPSID += +'([0-9]+)'", page, re.MULTILINE).group(1)
                sid = re.search(r"SUBSID += +'([0-9]+)'", page, re.MULTILINE).group(1)

        oos = tarscore.TarsOutputStream()
        oos.write(tarscore.int64, 0, int(ayuid))
        oos.write(tarscore.boolean, 1, True)  # Anonymous
        oos.write(tarscore.string, 2, "")  # sGuid
        oos.write(tarscore.string, 3, "")
        oos.write(tarscore.int64, 4, int(tid))
        oos.write(tarscore.int64, 5, int(sid))
        oos.write(tarscore.int64, 6, 0)
        oos.write(tarscore.int64, 7, 0)

        wscmd = tarscore.TarsOutputStream()
        wscmd.write(tarscore.int32, 0, 1)
        wscmd.write(tarscore.bytes, 1, oos.getBuffer())

        reg.append(wscmd.getBuffer())
        return HUYALIVE.wss_url, reg

    @staticmethod
    def decode_pak(data):
        class user(tarscore.struct):
            def readFrom(ios):
                return ios.read(tarscore.string, 2, False).decode("utf8")

        name, text = "", ""
        paks = []
        ios = tarscore.TarsInputStream(data)

        if ios.read(tarscore.int32, 0, False) == 7:
            ios = tarscore.TarsInputStream(ios.read(tarscore.bytes, 1, False))
            if ios.read(tarscore.int64, 1, False) == 1400:
                ios = tarscore.TarsInputStream(ios.read(tarscore.bytes, 2, False))
                name = ios.read(user, 0, False)
                text = ios.read(tarscore.string, 3, False).decode("utf8")

        if name != "":
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            pak = {"time": localtime, "username": name, "text": text, "pak_type": "normal_dm"}
            col.insert_one({localtime: [name, text]})

        else:
            pak = {"time": "", "username": "", "text": "", "pak_type": "unsupported_type"}
        paks.append(pak)
        return paks
