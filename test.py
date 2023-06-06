import streamlit as st
from datetime import datetime
import pandas as pd
from datetime import datetime
import math
import openpyxl

today = datetime.today()#获取日期
month_today = str(today.month)+'月'#获取月份
quarter_today = "Q"+str(math.ceil(today.month/3))#获取季度

st.title("数据小览")
st.header("出货数据")
st.subheader(f"{quarter_today}及{month_today}出货完成率")
df = pd.read_excel("省联动.xlsx",sheet_name="出货数据")
df = df.loc[:,"嘉兴地区年度目标数据":]
df.columns = df.iloc[0,:]
df = df.set_index(["城市","项目"])
df = df.fillna(0)
df = df.iloc[2:,:].astype("float64")
df = df.round(2)
col_me1,col_me2,col_me3 = st.columns(3)
col_me1.metric(
    label="嘉兴/海宁/桐乡",
    value=str(df[quarter_today].iloc[2]*100)+" %",
    delta=str(df[month_today].iloc[2]*100)+" %",
    )
col_me2.metric(
    label="平湖",
    value=str(df[quarter_today].iloc[12]*100)+" %",
    delta=str(df[month_today].iloc[12]*100)+" %",
    )
col_me3.metric(
    label="海盐",
    value=str(df[quarter_today].iloc[7]*100)+" %",
    delta=str(df[month_today].iloc[7]*100)+" %",)
st.dataframe(df)