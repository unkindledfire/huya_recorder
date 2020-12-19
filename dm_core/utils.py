# 传入 url:房间号 pak：队列
import asyncio

import aiohttp

from .huya import HUYALIVE


class ListenClient:
    def __init__(self, url, pak):
        self.__url = None
        self.__platform = HUYALIVE
        self.__dmpack = pak
        self.__exit = False
        self.__tiedup = True
        self.__heartbeat = None
        self.__websocket = None

        self.__url = "https://www.huya.com/" + url
        self.__heartbeat = aiohttp.ClientSession()

    async def init_ws(self):
        websocket, reg_info = await self.__platform.get_ws_info(self.__url)
        self.__websocket = await self.__heartbeat.ws_connect(websocket)
        if reg_info:
            for i in reg_info:
                await self.__websocket.send_bytes(i)

    async def heartbeats(self):
        while not self.__exit and self.__platform.heartbeat:
            await asyncio.sleep(self.__platform.heartbeatInterval)
            try:
                await self.__websocket.send_bytes(self.__platform.heartbeat)
            except:
                pass

    async def get_dm(self):
        while not self.__exit:
            async for i in self.__websocket:
                self.__tiedup = True
                for k in self.__platform.decode_pak(i.data):
                    await self.__dmpack.put(k)
            await asyncio.sleep(1)
            await self.init_ws()
            await asyncio.sleep(1)

    async def stop(self):
        self.__exit = True
        await self.__heartbeat.close()

    async def link_start(self):
        await self.init_ws()
        await asyncio.gather(self.heartbeats(), self.get_dm())
