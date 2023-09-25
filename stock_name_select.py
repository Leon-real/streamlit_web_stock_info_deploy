import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from pykrx import stock
import requests, json, time
from bs4 import BeautifulSoup
from datetime import datetime


today_date = str(datetime.today()).split(" ")[0].replace("-",'')
if datetime.today().weekday()==5:
    today_date = str(int(today_date)-1)
elif datetime.today().weekday() == 6:
    today_date = str(int(today_date)-2)
    
code = '005930'

# 종목명, 현재가 반환하기
def stock_info(code):
    # today_date = str(datetime.today()).split(" ")[0].replace("-",'')
    result = {}
    name = stock.get_market_ticker_name('005930')
    price, _ = get_price(code)
    
    result['종목명']=name
    result['현재가']=price
    return result

# 오늘의 국내 모든 주식 정보 dataframe
def todays_list():
    # today_date = str(datetime.today()).split(" ")[0].replace("-",'')
    stock_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="ALL")}) # KOSPI, KOSDAQ, KONEX, ALL, (default=KOSPI)
    stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
    stock_fud = pd.DataFrame(stock.get_market_fundamental_by_ticker(date=today_date, market="ALL"))
    stock_fud = stock_fud.reset_index()
    stock_fud.rename(columns={'티커':'종목코드'}, inplace=True)
    result = pd.merge(stock_list, stock_fud, left_on='종목코드', right_on='종목코드', how='outer')
    stock_price = stock.get_market_ohlcv_by_ticker(date=today_date, market="ALL")
    stock_price = stock_price.reset_index()
    stock_price.rename(columns={'티커':'종목코드'}, inplace=True)
    result1 = pd.merge(result, stock_price, left_on='종목코드', right_on='종목코드', how='outer')
    result1 = result1.replace([0], np.nan)
    result1 = result1.dropna(axis=0)
    result1['내재가치'] = (result1['BPS'] + (result1['EPS']) * 10) / 2
    result1['내재가치/종가'] = (result1['내재가치'] / result1['종가'])

    print(f"Complete {len(result1)}")
    
    return result1

# 가격 정보 크롤링
def get_price(company_code):
    bs_obj, url = get_code(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})
    now_price = blind.text
    return now_price, url

# 종목코드로 웹 크롤링
def get_code(company_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj, url