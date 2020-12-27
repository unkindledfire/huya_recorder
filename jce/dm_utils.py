import urllib3
from .dm import HUYA_DM

class ListenClient:
    def __init__(self,id):
        self.__url = "https://www.huya.com/" + url
        self.__heartbeat = urllib3.PoolManager()
        self.__tiedup = True
        self.__exit = False
        self.__websocket = None
        self.__platform = HUYA_DM

    def init_ws(self):
        websocket, reg_info =