import streamlit as st
from datetime import datetime
import pandas as pd
import datetime
import math
import openpyxl

today = datetime.datetime.today()#获取日期
month_today = str(today.month)+'月'#获取月份
quarter_today = "Q"+str(math.ceil(today.month/3))#获取季度

st.title("数据小览")
st.header("出货数据")
df = pd.read_excel("省联动.xlsx",sheet_name="出货数据")
df = df.loc[:,"嘉兴地区年度目标数据":]
df.columns = df.iloc[0,:]
col_me1,col_me2,col_me3 = st.columns(3)
col_me1.metric(
    label="嘉兴/海宁/桐乡",
    value=str(int(df[quarter_today].iloc[3]))+" %",
    delta=str(int(df[month_today].iloc[3]))+" %"
    )
col_me1.metric(
    label="平湖",
    value=str(int(df[quarter_today].iloc[14]))+" %",
    delta=str(int(df[month_today].iloc[14]))+" %"
    )
col_me1.metric(
    label="海盐",
    value=str(int(df[quarter_today].iloc[9]))+" %",
    delta=str(int(df[month_today].iloc[9]))+" %"
    )

start_time = st.slider(
    "When do you start?",
    value=datetime(2020, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)