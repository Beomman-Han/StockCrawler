from abc import ABC, abstractmethod

class MarketInvestor(ABC):
    """웹 크롤링을 통해 시장에 상장된 주식회사의 재무, 주가 정보를 조사한다.
    """

    @property
    @abstractmethod
    def market(self) -> str:
        """클래스의 market 속성에 접근하는 getter 메소드"""
        pass

    @market.setter
    @abstractmethod
    def market(self, market_name: str) -> None:
        """클래스의 market 속성을 설정하는 setter 메소드"""
        pass



