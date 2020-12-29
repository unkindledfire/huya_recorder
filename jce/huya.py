import asyncio
import re
import aiohttp
from .tars import tarscore

class HUYA:
    def __init__(self):
        self.__ws = 'wss://cdnws.api.huya.com/'
        self.__hb = b'\x00\x03\x1d\x00\x00\x69\x00\x00\x00\x69\x10\x03\x2c\x3c\x4c\x56\x08\x6f\x6e\x6c\x69\x6e\x65\x75\x69\x66\x0f\x4f\x6e\x55\x73\x65\x72\x48\x65\x61\x72\x74\x42\x65\x61\x74\x7d\x00\x00\x3c\x08\x00\x01\x06\x04\x74\x52\x65\x71\x1d\x00\x00\x2f\x0a\x0a\x0c\x16\x00\x26\x00\x36\x07\x61\x64\x72\x5f\x77\x61\x70\x46\x00\x0b\x12\x03\xae\xf0\x0f\x22\x03\xae\xf0\x0f\x3c\x42\x6d\x52\x02\x60\x5c\x60\x01\x7c\x82\x00\x0b\xb0\x1f\x9c\xac\x0b\x8c\x98\x0c\xa8\x0c'
        self.__hb_interval = 60

    async def get_ws(self,roomid):
        secret = []
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.88 Mobile Safari/537.36'
        }
        async with aiohttp.ClientSession() as s:
            async with s.get('https://m.huya.com/'+str(roomid),headers=headers) as res:
                page_plaintext = await res.text()
                ayyu = re.search(r"ayyuid: +'([0-9]+)'", page_plaintext, re.MULTILINE).group(1) if re.search(r"ayyuid: +'([0-9]+)'", page_plaintext, re.MULTILINE) is not None else None
                tops = re.search(r"TOPSID += +'([0-9]+)'", page_plaintext, re.MULTILINE) if re.search(r"TOPSID += +'([0-9]+)'", page_plaintext, re.MULTILINE) is not None else None
                subs = re.search(r"SUBSID += +'([0-9]+)'", page_plaintext, re.MULTILINE) if re.search(r"SUBSID += +'([0-9]+)'", page_plaintext, re.MULTILINE) is not None else None

        #构造JCE
        jce = tarscore.TarsOutputStream()
        jce.write(tarscore.int64,0,int(ayyu))
        jce.write(tarscore.boolean,1,True)
        jce.write(tarscore.string,2,"")
        jce.write(tarscore.string,3,"")
        jce.write(tarscore.int64,4,int(tops))
        jce.write(tarscore.int64,5,int(subs))
        jce.write(tarscore.int64,6,0)
        jce.write(tarscore.int64,7,0)

        wscmd = tarscore.TarsOutputStream()
        wscmd.write(tarscore.int32,0,1)
        wscmd.write(tarscore.bytes,1,jce.getBuffer())

        secret.append(wscmd.getBuffer())
        return self.__ws, secret
    def decode_dm(self,dm):
        class user(tarscore.struct):
            def
class DM_LIVE:
    def __init__(self,roomid):
        self.__roomID = str(roomid)
        self.__flag = False
        self.headers = {

        }