import os
import requests
from typing import Dict, List
import json


class Driver:
    DATA_URL: str = "https://data.alpaca.markets/v1"
    BASE_URL: str = "https://paper-api.alpaca.markets/v2"

    def __init__(self):
        self.__api_key: str = os.getenv("API_KEY")
        self.__secret: str = os.getenv("SECRET")

    def __get(self, path: str, base=False) -> requests.Response:
        payload: Dict[str, str] = {"APCA-API-KEY-ID": self.__api_key, "APCA-API-SECRET-KEY": self.__secret}
        url: str = "{}/{}".format(Driver.BASE_URL if base else Driver.DATA_URL, path)
        return requests.get(url, headers=payload)

    def daily(self, symbols: List[str] = None, limit: int = 100) -> Dict:
        response: requests.Response = self.__get("bars/1D?symbols=%s&limit=%d" % (",".join(symbols), limit))
        return json.loads(response.content)

    def assets(self) -> List[str]:
        response: requests.Response = self.__get("assets?status=active", True)
        data: List[Dict[str, str]] = json.loads(response.content)
        return [stock["symbol"] for stock in data]
