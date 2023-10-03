import stock_name_select
import chart_and_predict_stock

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

from datetime import datetime


# 페이지 기본 설정
st.set_page_config(
    page_icon='📈',
    page_title='주식 정보',
    layout='wide',
)

# 페이지 헤더, 서브헤더 제목 설정
st.header("주식 정보 홈페이지에 오신걸 환영합니다.")
st.subheader("맛 보기")

# 종목별 정보 저장하기
@st.cache_data
def load_data():
    df = stock_name_select.todays_list().set_index('종목코드')
    return df
df = load_data()

# 개별 주식 종목 정보 조회하기
code = st.text_input('주식코드 or 종목명', '005930')
if code.isdigit()==False:
    code = (df.loc[df['종목명']==code.upper()].index)[0]
    # print(f"{code} 조회")
    
# 정보 조회하기 버튼 클릭시
if st.button("정보 조회하기"):
    with st.spinner("정보 조회중 . . ."):
        result = stock_name_select.stock_info(code)
        st.write(f"{result['종목명']} {result['현재가']}") # 현재가 작성하기
        target_df = df.loc[df['종목명']==result['종목명']] # 타겟 데이터 프레임 조회
        st.pyplot(chart_and_predict_stock.show_chart(code)) # 차트 그려서 보여주기
        st.plotly_chart(chart_and_predict_stock.show_chart_ver_2(code))
        st.dataframe(target_df) # 데이터 프레임 보여주기
        
        
# 오늘 일자로 전체 종목 정보 불러오기
st.subheader("국내 모든 주식 정보 보기")
with st.spinner("정보 조회중 . . ."):
    # 데이터 프레임 생성하기
    st.table(df)
    # # 페이지 번호를 선택할 수 있는 컨트롤 추가
    # page_number = st.slider('페이지 번호', 1, len(df) // 10 + 1, 1)

    # # 선택한 페이지의 데이터 표시
    # start_idx = (page_number - 1) * 10
    # end_idx = start_idx + 10
    # st.dataframe(df.iloc[start_idx:end_idx])
    
# 조회할 날짜 선택하기
col0,col1 = st.columns(2)
with col0:
    start_date = st.date_input('Start', value=pd.to_datetime('today'))
with col1:
    end_date = st.date_input('End', value=pd.to_datetime('today'))
# 날짜 뒤바뀔 경우 순서 바꿔주기
if sum([int(x)*y for x,y in zip(str(start_date).split("-"), [12,31,1])]) <= sum([int(x)*y for x,y in zip(str(end_date).split("-"), [12,31,1])]):
    pass
else:
    temp_date= start_date
    start_date = end_date
    end_date = temp_date
    print("Change Start_date and End_date to prevent Error")
tickers = df['종목명']
tickers_dropdown_prices = st.multiselect('종목 선택하기', tickers)

# 종목을 선택했을 때 각 종목의 종가 한 그래프에 보여주기
if len(tickers_dropdown_prices)>0: 
    tmp_df=pd.DataFrame()
    for ticker_dropdown_prices in tickers_dropdown_prices:
        select_code = (df.loc[df['종목명']==ticker_dropdown_prices].index)[0]
        tmp_df[ticker_dropdown_prices] = chart_and_predict_stock.get_data(select_code, start_date, end_date)['Close']
        # print(tmp_df)
        # print(select_code)
    st.line_chart(tmp_df)