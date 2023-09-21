import stock_name_select

import streamlit as st
import statsmodels.api as sm # 회기모델 
import pandas as pd
import numpy as np
import yfinance as yf

from datetime import datetime
from dateutil.relativedelta import relativedelta


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
df = stock_name_select.todays_list().set_index('종목코드')

# 개별 주식 종목 정보 조회하기
code = st.text_input('주식코드', '005930')
if st.button("정보 조회하기"):
    with st.spinner("정보 조회중 . . ."):
        result = stock_name_select.stock_info(code)
        st.write(f"{result['종목명']} {result['현재가']}") # 현재가 작성하기
        target_df = df.loc[df['종목명']==result['종목명']] # 타겟 데이터 프레임 조회
        
        st.dataframe(target_df) # 데이터 프레임 보여주기
        
        
# 오늘 일자로 전체 종목 정보 불러오기
st.subheader("국내 모든 주식 정보 보기")
with st.spinner("정보 조회중 . . ."):
    # 페이지 번호를 선택할 수 있는 컨트롤 추가
    page_number = st.slider('페이지 번호', 1, len(df) // 10 + 1, 1)

    # 선택한 페이지의 데이터 표시
    start_idx = (page_number - 1) * 10
    end_idx = start_idx + 10
    st.dataframe(df.iloc[start_idx:end_idx])
    
    