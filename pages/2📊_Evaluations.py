import streamlit as st
import pandas as pd
import numpy as np
import stock_name_select

# 페이지 기본 설정
st.set_page_config(
    page_icon='📊',
    page_title='종목별 평가',
    layout='wide',
)
# 종목별 정보 저장하기
@st.cache_data
def load_data():
    df = stock_name_select.todays_list().set_index('종목코드')
    return df
df = load_data()


# 페이지 헤더, 서브헤더 제목 설정
st.header("종목별 분석")


# 저평가, 고평가 부분
st.subheader("가치주 평가")

st.subheader("조건 선택하기")
col0,col1,col2,col3,col4,col5 = st.columns(6)
with col0:
    BPS_check = st.checkbox("BPS")
with col1:
    PER_check = st.checkbox("PER")
with col2:
    PBR_check = st.checkbox("PBR")
with col3:
    EPS_check = st.checkbox("EPS")
with col4:
    DIV_check = st.checkbox("DIV")
with col5:
    DPS_check = st.checkbox("DPS")
    
    
check_lists=[]
if BPS_check:
    check_lists.append("BPS")
if PER_check:
    check_lists.append("PER")
if PBR_check:
    check_lists.append("PBR")
if EPS_check:
    check_lists.append("EPS")
if DIV_check:
    check_lists.append("DIV")
if DPS_check:
    check_lists.append("DPS")
    
df_pivot = df[['종목명','종가','BPS','PER','PBR','EPS','DIV','DPS']]
st.subheader("DataFrame 보여주기")
st.markdown(f'''
            - {check_lists} 항목 중, 밸류에이션이 낮은 20개 종목 나타내기
            - 순위 구하는 방법
                1. 선택된 항목을 순서대로 순위 구하기
                2. 나온 순위를 더하여서 랭킹 다시 구하기
                3. 랭킹이 낮은 항목 20개(저평가 되었다고 가정하고.)표시
            ''')
if len(check_lists)>0:
    value_rank = df_pivot[check_lists].rank(axis = 0) #열을 선택한 후 , 각열을 기준으로 순위를 구함
    value_sum = value_rank.sum(axis = 1, skipna = False).rank() #더해진 값으로 랭킹을 다시 구함
    value = df_pivot.loc[value_sum <= 20] # 밸류에이션이 낮은 20개 종목
    st.dataframe(value) # 데이터 프레임 보여주기
st.markdown(f'''
            - {check_lists} 항목 중, 밸류에이션이 높은 20개 종목 나타내기
            - 순위 구하는 방법
                1. 선택된 항목을 순서대로 순위 구하기
                2. 나온 순위를 더하여서 랭킹 다시 구하기
                3. 랭킹이 높은 항목 20개(고평가 되었다고 가정하고.)표시
            ''')
if len(check_lists)>0:
    value_rank = df_pivot[check_lists].rank(axis = 0) #열을 선택한 후 , 각열을 기준으로 순위를 구함
    value_sum = value_rank.sum(axis = 1, skipna = False).rank() #더해진 값으로 랭킹을 다시 구함
    value = df_pivot.loc[value_sum > value_sum.max()-20] # 밸류에이션이 높은 20개 종목
    st.dataframe(value) # 데이터 프레임 보여주기
