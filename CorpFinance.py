
class CorpFinance(object):
    """기업의 재무정보(및 시총 등)를 저장하기 위한 클래스

    최근 3개년의 매출액, 영업이익, 당기이익, 영업이익률, 당기이익률,
    ROE, 부채비율, 당좌비율, PER, PBR 정보를 저장한다.
    * 매출액, 영업이익, 당기이익: (억원)
    * 영업이익률, 당기이익률, ROE, 부채비율, 당좌비율: (%)
    * PER, PBR: (배)

    Attributes
    ----------

    corp_name: str
        기업명
    corp_code: str
        기업 고유 번호
    stock_code: str
        상장 주식 고유 번호
    market_capital: int
        시가총액
    revenue: dict of (str: int)
        매출액
    operating_income: dict of (str: int)
        영억이익
    net_profit: dict of (str: int)
        당기이익
    operating_income_rate: dict of (str: float)
        영업이익률(%)
    net_profit_rate: dict of (str: float)
        당기이익률(%)
    roe: dict of (str: float)
        ROE(%), 자기자본수익률
    liability_rate: dict of (str: float)
        부채비율(%)
    quick_rate: dict of (str: float)
        당좌비율(%)
    per: dict of (str: float)
        PER(배), 주가수익률
    pbr: dict of (str: float)
        PBR(배), 주가순자비율
    """

    def __init__(self, corp_name: str,
                 corp_code: str,
                 stock_code: str):

        self.corp_name = corp_name
        self.corp_code = corp_code
        self.stock_code = stock_code

        ## Empty
        self.market_capital = None
        self.stocks_listed = None
        self.revenue = None
        self.operating_income = None
        self.net_profit = None
        self.operating_income_rate = None
        self.net_profit_rate = None
        self.roe = None
        self.liability_rate = None
        self.quick_rate = None
        self.per = None
        self.pbr = None

    def set_market_cap(self, val: str) -> None:
        """현재 시점의 시가총액을 저장

        Parameters
        ----------
        val: int
            시가총액
        """
        self.market_capital = val
        return

    def set_stocks_listed(self, val: int) -> None:
        """현재 시점의 상장주식수를 저장

        Parameters
        ----------
        val: int
            상장주식수
        """
        self.stocks_listed = val
        return

    def set_revenue(self, val: dict) -> None:
        """최근 3개년의 매출액을 저장

        Parameters
        ----------
        val: dict of (str: int)
            3개년의 (년도:매출액)
        """
        self.revenue = val
        return

    def set_operating_income(self, val: dict) -> None:
        """최근 3개년의 영업이익을 저장

        Parameters
        ----------
        val: dict of (str: int)
            3개년의 (년도:영업이익)
        """
        self.operating_income = val
        return

    def set_operating_income_rate(self, val: dict) -> None:
        """최근 3개년의 영업이익률을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:영업이익률)
        """
        self.operating_income_rate = val
        return

    def set_net_profit(self, val: dict) -> None:
        """최근 3개년의 당기순이익을 저장

        Parameters
        ----------
        val: dict of (str: int)
            3개년의 (년도:당기순이익)
        """
        self.net_profit = val
        return

    def set_net_profit_rate(self, val: dict) -> None:
        """최근 3개년의 당기순이익률을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:당기순이익률)
        """
        self.net_profit_rate = val
        return

    def set_roe(self, val: dict) -> None:
        """최근 3개년의 roe(자기자본수익률)을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:자기자본수익률)
        """
        self.roe = val
        return

    def set_liability_rate(self, val: dict) -> None:
        """최근 3개년의 liability(부채비율)을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:부채비율)
        """
        self.liability_rate = val
        return

    def set_quick_rate(self, val: dict) -> None:
        """최근 3개년의 당좌비율을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:당좌비율)
        """
        self.quick_rate = val
        return

    def set_per(self, val: dict) -> None:
        """최근 3개년의 per을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:주가수익비율)
        """
        self.per = val
        return

    def set_pbr(self, val: dict) -> None:
        """최근 3개년의 pbr을 저장

        Parameters
        ----------
        val: dict of (str: float)
            3개년의 (년도:순자산가치배율)
        """
        self.pbr = val
        return

    ## FIXME 성장률 계산, 동종업계 속성 추가

    def __str__(self) -> str:
        """print(CorpFinance) 시 출력 내용"""

        explain = f'Instance of CorpFinance class\n'
        explain += f'-----------------------------\n'
        explain += f'회사명: {self.corp_name}\n'
        explain += f'회사코드: {self.corp_code}\n'
        explain += f'상장코드: {self.stock_code}\n'
        explain += f'시가총액(억원): {self.market_capital}\n'
        explain += f'상장주식수: {self.stocks_listed}\n'
        explain += f'매출액(억원): {self.revenue}\n'
        explain += f'영업이익(억원): {self.operating_income}\n'
        explain += f'영업이익률(%): {self.operating_income_rate}\n'
        explain += f'당기순이익(억원): {self.net_profit}\n'
        explain += f'당기순이익률(%): {self.net_profit_rate}\n'
        explain += f'부채비율(%): {self.liability_rate}\n'
        explain += f'당좌비율(%): {self.quick_rate}\n'
        explain += f'ROE(%): {self.roe}\n'
        explain += f'PER(배): {self.per}\n'
        explain += f'PBR(배): {self.pbr}\n'

        return explain

    def __repr__(self) -> str:
        return f'Instance of CorpFinance class...\nFor detail info, print() function.'

if __name__ == '__main__':

    print(f'> [WARNING] This code is not intended for funning script...')
    print(f'> [WARNING] We recommend using this code at other running scripts...')
    print(f'> [WARNING] Anyway... Running...')
    #help(CorpFinance)
    #corp_fin = CorpFinance('', '', '')
    #print(corp_fin)
    #print(CorpFinance)