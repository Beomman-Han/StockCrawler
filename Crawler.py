from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class Crawler(ABC):
    """웹 url을 통해 필요한 정보를 크롤링한다."""

    def __init__(self, url:str) -> None:
        self.url = url

    def receive_req(self):
        """url으로부터 request를 받는다."""
        req = requests.get(self.url)
        if req.status_code != '200':
            print(f'Invalid request: {req.status_code}')

        return

    @property
    @abstractmethod
    def url(self) -> str:
        """self._url getter method"""
        return self._url

    @url.setter
    @abstractmethod
    def url(self, _url:str) -> None:
        """self._url setter method"""
        self._url = _url
        return
