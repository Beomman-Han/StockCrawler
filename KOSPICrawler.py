import os, sys

import bs4

from Crawler import Crawler
import dart_fss as dart
from datetime import date
import requests
from bs4 import BeautifulSoup
#from collections import OrderedDict
from CorpFinance import CorpFinance

class CorpInfo(object):
    
    def __init__(self,
        corp_code : str,
        corp_name : str,
        stock_code : str,
        update_date : str
        ) -> None:
        
        self.corp_code = corp_code
        self.corp_name = corp_name
        self.stock_code = stock_code
        self.update_date = update_date
        
        return

class KOSPICrawler(Crawler):
    """KOSPI 종목 관련 재무 정보를 크롤링하기 위한 클래스
    """
    
    KOSPI_CODE = 'Y'

    def __init__(self, csv: str) -> None:
        """Initialize KOSPICrawler class 
        
        Parameters
        ----------
        csv : str
            Path of .csv file containing corp info
        """
        
        # self.stock_data = './data/test_samsung.2021-12-12.csv'
        self.csv = csv
        
        return

    def _load_corp_info(self) -> list:
        """DB에서 기업명,코드 등의 정보를 로딩한다.

        Returns
        -------
        list of tuples of str
            (기업코드,회사명,종목코드,수정일)의 리스트
        """

        set_corps = set()
        kospi_db = [ f'{self._STOCK_DB}/{file}' for file in os.listdir(self._STOCK_DB) if file.startswith('kospi') ]
        for csv_ in kospi_db:
            print(f'> Load KOSPI DB: {kospi_db}...')
            csv = open(csv_, 'r', encoding='utf8')
            header = csv.readline()
            for line in csv:
                cols = line.strip().split(',')
                set_corps.add((cols[0],cols[1],cols[2],cols[3]))
            csv.close()
        corps = sorted(list(set_corps), key=lambda x:x[1])

        return corps

    def _set_api_key(self) -> None:
        """DART Open 서비스 이용을 위한 api_key 입력"""
        dart.set_api_key(api_key='1bf8a5d812f3e051f08b1cb262b4b4bd6c9b1ced')
        return

    def _response_url(self, url, params_: dict) -> requests.models.Response:
        """url request를 보내 response를 받음.

        Parameters
        ----------
        url: str
            Response를 받을 기본 url 주소
        params_: dict
            requests.get 메소드를 실행할 파라미터를 포함한 딕셔너리

        Returns
        -------
        requests.models.Response
            기본 url에 대한 Response 객체 status가 비정상일 경우 None Response 리턴
        """

        param  = params_['param']
        header = params_['header']
        response = requests.get(url, params=param, headers=header)
        #print(response.status_code)
        if response.status_code != 200:
            response = requests.models.Response()

        return response

    def _parse_soup(self, soup: bs4.BeautifulSoup):

        pass

        return

    def run_naver(self):
        """네이버 금융 페이지에서 기업 정보를 크롤링한다.
        기본 설정된 DB 경로에 KOSPI 종목 정보를 가져와서 크롤링을 진행한다.
        """

        corp_list = self._load_corp_info()
        self.crawl_naver_fin(corp_list)

        return

    def crawl_naver_fin(self, corps: list) -> None:
        """기업 리스트를 받아 네이버 금융 페이지에서 크롤링 작업을 진행한다.

        Parameters
        ----------
        corps: list of tuples
            (기업코드, 기업명, 상장코드, 수정일) 리스트
        """

        for curr, corp in enumerate(corps):
            corp_code = corp[0]
            corp_name = corp[1]
            stock_code = corp[2]
            print(f'> Process {curr+1}th corp: {corp_name}...')
            corp_info = self._scrap_naver_fin_page(corp_code, corp_name, stock_code)
            print(corp_info)

        return

    def _soup_get_text(self, soup: BeautifulSoup, css_selector: str) -> str or None:
        """soup 객체로부터 원하는 값을 가져오도록 한다.
        예외 발생 시 처리하는 것이 주목적.

        soup: BeautifulSoup
            soup 객체 (html parser)
        css_selector: str
            soup 객체로부터 parsing하기 위한 키 값 (css 선택자로 파싱함.)
        """

        tag = soup.select_one(css_selector)
        if tag is None:
            return None

        tag_text = tag.get_text().strip().replace('\t','').replace('\n','')
        if tag_text == '':
            return None

        return tag_text

    def _numeric(self, text: str) -> int or float or None:

        try:
            val = int(text)
        except ValueError:
            try:
                val = float(text)
            except ValueError:
                val = None

        return val

    def _scrap_naver_fin_page(self, corp_code: str, corp_name: str, stock_code: str) -> CorpFinance:
        """주식 코드를 받아 네이버 금융 사이트에서 관련 정보를 수집한다.
        수집할 정보는 다음과 같다.
        > 시가총액, 상장주식수, PER, PBR, 동일업종 PER,
          (3년) 매출액, 영업이익, 당기순이익,
          영업이익률, 순이익률, ROE(**),
          부채비율, 당좌비율, PER, PBR

        FIXME 추가해야 할 정보
        > (최근 분기) 매출액, 영업이익, 당기순이익,
        영억이익률, 순이익률, ROE(**),
        부채비율, 당좌비율, PER, PBR

        FIXME + 위 정보를 포함할 데이터 저장용 클래스를 생성 (FinanceInfo())

        Parameters
        ----------
        corp_code: str
            기업 고유 코드번호
        corp_name: str
            기업 이름
        stock_code: str
            주식 고유 코드번호

        Returns
        -------
        CorpFinance
            각 정보(재무정보 포함)가 포함된 CorpFinance 클래스
        """

        print(f'> Scrap naver page: {corp_name}, {corp_code}, {stock_code}')
        #corp_info = OrderedDict()

        basic_url = 'https://finance.naver.com/item/main.naver'
        ## 외부 프로그램이 아닌 정상적인 형태로 접근하는 것처럼 보이게 함(?)
        header = {'User-Agent': 'Mozilla/5.0', 'referer': 'http://naver.com'}
        param  = {'code': stock_code}
        response = self._response_url(basic_url, {'header': header, 'param': param})
        print(f'response status code: {response.status_code}')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            return CorpFinance('', '', '')

        corp_fin = CorpFinance(corp_name, corp_code, stock_code)

        ## 정상 금융 정보 페이지인지 확인
        """
        css_selector = '#middle > div.h_company > div.wrap_company > h2 > a'
        try:
            chk = soup.select_one(css_selector).get_text().strip()
        except AttributeError:
        """

        ## 시가총액 및 상장주식수
        """
        try:
            market_capital = soup.select_one('#_market_sum').get_text()
            market_capital = int(market_capital.strip().replace('\n', '').replace('\t', '').replace(',', '').replace('조', ''))
        except AttributeError:
            market_capital = None
        if market_capital is not None:
            if '경' in market_capital:
                market_capital = 100000000  ## 경 이상...?
            elif '조' in market_capital:
                market_capital = market_capital.replace(',','').split('조')
                if len(market_capital) == 2:
                    market_capital = 1000*int(market_capital[0]) + int(market_capital[1])
        #print(f'Market capital: {market_capital}')
        
        try:
            stocks_listed = soup.select_one('#tab_con1 > div.first > table > tr:nth-of-type(3) > td > em').get_text()
            stocks_listed = int(stocks_listed.strip().replace(',','').replace('\n','').replace('\t',''))
        except AttributeError:
            stocks_listed = None        
        """

        market_capital = self._soup_get_text(soup, '#_market_sum')

        css_selector  = '#tab_con1 > div.first > table > tr:nth-of-type(3) > td > em'
        stocks_listed = self._soup_get_text(soup, css_selector)
        if stocks_listed is not None:
            stocks_listed = int(stocks_listed.replace(',',''))

        corp_fin.set_market_cap(market_capital)
        corp_fin.set_stocks_listed(stocks_listed)

        if market_capital is not None and stocks_listed is not None:
            css_corp_analysis = f'div.section.cop_analysis'

            ## 과거 3개년 년도
            """
            > 과거 3개년 연도 정보
            '#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child(1)'
            '#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child(2)'
            '#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child(3)'
    
            > 최근 5개 분기 분기 정보
            '#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child(5)'
            '#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child(6)'
            ...
            
            '#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child(1)'    
            """
            years = []
            for i in range(1, 4):
                css_selector = f'{css_corp_analysis} > div.sub_section > table > thead > tr:nth-of-type(2) > th:nth-of-type({i})'
                year = self._soup_get_text(soup, css_selector)
                years.append(year)
            #print(years); sys.exit()

            """
            > 재무정보 단위 (억원??)
            매출액:    '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(1) > th'
            영억이익:   '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(2) > th'
            당기순이익: '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > th'
            
            financial_info = ['매출액', '영업이익', '당기순이익',\
                              '영업이익률', '순이익률', 'ROE',\
                              '부채비율', '당좌비율', 'PER', 'PBR']
            #first_fin = ['매출액', '영업이익', '당기순이익']
            for i in range(1, 9):
                css_selector = f'div.sub_section > table > tbody > tr:nth-child({i}) > th'
                unit = corp_analysis.select_one(css_selector)
                unit = unit.get_text().strip()
            """
            """
            > 과거 3년 주요 재무정보
            매출액: '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(1) > td:nth-child(2,3,4)'
            영업익: '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(2) > td:nth-child(2,3,4)'
            당기익: '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(3) > td:nth-child(2,3,4)'
            """
            financial_item = ['revenue', 'operating_income', 'net_profit',\
                              'operating_income_rate', 'net_profit_rate',\
                              'roe', 'liability_rate', 'quick_rate', 'per', 'pbr']

            """
            '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(1) > td:nth-child(2)'
            '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(2) > td:nth-child(2)'
            '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(11) > td:nth-child(2)'
            '#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(13) > td:nth-child(2)'
            #content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(11) > td:nth-child(2)
            """
            total_fin_info = dict()
            for f_idx, item in enumerate(financial_item):
                if item == 'per':
                    item_css_selector = f'{css_corp_analysis} > div.sub_section > table > tbody > tr:nth-of-type({11})'
                elif item == 'pbr':
                    item_css_selector = f'{css_corp_analysis} > div.sub_section > table > tbody > tr:nth-of-type({13})'
                else:
                    item_css_selector = f'{css_corp_analysis} > div.sub_section > table > tbody > tr:nth-of-type({f_idx+1})'
                each_fin_info = dict()
                for y_idx, year in enumerate(years):
                    css_selector = f'{item_css_selector} > td:nth-of-type({y_idx+1})'
                    #tag = soup.select_one(css_selector)
                    tag = self._soup_get_text(soup, css_selector)
                    if tag is not None:
                        tag = tag.replace(',','')
                        tag = self._numeric(tag)
                    """
                    try:
                        tag_text = tag.get_text().strip().replace(',', '')  ## '2,437,714' -> '2437714'
                    except AttributeError:
                        tag_text = None
                        tag_val  = None
                        each_fin_info[year] = tag_val
                        continue

                    if tag_text == '':
                        each_fin_info[year] = None
                        continue

                    try:
                        tag_val = int(tag_text)
                    except ValueError:
                        tag_val = float(tag_text)
                    """
                    each_fin_info[year] = tag
                total_fin_info[item] = each_fin_info

            corp_fin.set_revenue(total_fin_info['revenue'])
            corp_fin.set_operating_income(total_fin_info['operating_income'])
            corp_fin.set_operating_income_rate(total_fin_info['operating_income_rate'])
            corp_fin.set_net_profit(total_fin_info['net_profit'])
            corp_fin.set_net_profit_rate(total_fin_info['net_profit_rate'])
            corp_fin.set_roe(total_fin_info['roe'])
            corp_fin.set_liability_rate(total_fin_info['liability_rate'])
            corp_fin.set_quick_rate(total_fin_info['quick_rate'])
            corp_fin.set_per(total_fin_info['per'])
            corp_fin.set_pbr(total_fin_info['pbr'])

        return corp_fin

    @property
    def url(self) -> str:
        """url getter method"""
        return self._url

    @url.setter
    def url(self, _url: str) -> None:
        self._url = _url
        return

def _set_api_key() -> None:
    """DART Open 서비스 이용을 위한 api_key 입력"""
    dart.set_api_key(api_key='1bf8a5d812f3e051f08b1cb262b4b4bd6c9b1ced')
    return

def load_corp_code() -> None:
    """KOSPI 상장 종목의 회사명, 회사코드, 주식코드를 DB에 업데이트한다.
    매번 실행할 필요는 없고, 분기별 혹은 매년 업데이트 시 사용된다.
    KOSPICrawler 클래스에는 포함되지 않도록 밖으로 뺌.
    (주의) 하루에 10,000 번 이상 DART 서버에 요청 불가능...

    FIXME 시간 소요 많음... (시간 체크 필요)

    DB 형식은 .csv 형식으로 [DB_PATH]/kospi_list.[date].csv 명으로 저장된다.
    DB 내에는 'corp_name,corp_code,stock_code' 형식으로 코스피 기업 목록이 정리되어 있다.

    Parameters, Returns
    -------------------
    None
    """

    _STOCK_DB  = '/Users/hanbeomman/Documents/stock/DB'
    _DATE      = date.today().isoformat()  ## EX) '2021-12-12'
    KOSPI_CODE = 'Y'
    #global _STOCK_DB; global _DATE;

    kospi_f = open(f'{_STOCK_DB}/kospi_list.{_DATE}.csv', 'w', encoding='utf8')
    kospi_f.write('corp_name,corp_code,stock_code\n')
    #kospi_list = []  ## list of tuple(corp_name, corp_code, stock_code)

    _set_api_key()
    corp_list = dart.get_corp_list()
    corp_list = corp_list.corps
    for curr, corp in enumerate(corp_list):
        if (curr+1)%100 == 0:
            print(f'> Process {curr+1} corps...')

        corp_info = corp.load()  ## DART 서버에 요청
        market = corp_info['corp_cls']
        if market == KOSPI_CODE:
            print(f'> Find KOSPI corp!')
            corp_name  = corp_info['corp_name']
            corp_code  = corp_info['corp_code']
            stock_code = corp_info['stock_code']
            #kospi_list.append((corp_name, corp_code, stock_code))
            kospi_f.write(f'{corp_name},{corp_code},{stock_code}\n')
    kospi_f.close()

    return

if __name__ == '__main__':
    print(f'> [WARNING] This code is not intended for running script...')
    print(f'> [WARNING] We recommend using this code at other running scripts...')
    print(f'> [WARNING] Anyway... Running...')

    ## decorator, generator,

    #url = 'https://finance.naver.com/item/main.naver?code=005930'
    #KOSPICrawler(url)
    #load_corp_code()
    # crawler = KOSPICrawler()
    #crawler.run_naver()
    #corp = crawler._scrap_naver_fin_page('00177816','대주전자재료','078600')
    #corp = crawler._scrap_naver_fin_page('00126308','삼성엔지니어링','028050')
    ## 개별 종목 이름으로 검색하기 추가, 2021년 스탯 추가, 동종업계 PER 추가, 동종업계 추가, 성장률, 구글 기사 스크랩
    #corp = crawler._scrap_naver_fin_page('00138224','쌍용씨앤이','003410')
    #corp = crawler._scrap_naver_fin_page('00162461','한화솔루션','009830')
    #corp = crawler._scrap_naver_fin_page('00159616', '두산중공업', '034020')
    #corp = crawler._scrap_naver_fin_page('01199550', '현대에너지솔루션', '322000')
    # print(corp)