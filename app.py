import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_icon='📈',
    page_title='주식 정보',
    layout='wide',
)

# 페이지 헤더, 서브헤더 제목 설정
st.header("주식 정보 홈페이지에 오신걸 환영합니다.")
st.subheader("맛 보기")


code = st.text_input('주식코드', '005930')
if st.button("정보 조회하기"):
    with st.spinner("정보 조회중 . . ."):
        st.write("정보 조회중")