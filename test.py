import streamlit as st
from datetime import datetime
import pandas as pd
from datetime import datetime
import math
import openpyxl
import time

today = datetime.today()#获取日期
month_today = str(today.month)+'月'#获取月份
quarter_today = "Q"+str(math.ceil(today.month/3))#获取季度

def ch_data():
    # 出货数据
    st.header("出货数据")
    st.subheader(f"{quarter_today}及{month_today}出货完成率")
    df = pd.read_excel("省联动.xlsx",sheet_name="出货数据")
    df = df.loc[:,"嘉兴地区年度目标数据":]
    df.columns = df.iloc[0,:]
    df = df.set_index(["城市","项目"])
    df = df.fillna(0)
    df = df.iloc[2:,:].astype("float64")
    df = df.round(2)
    col_me0,col_me1,col_me2,col_me3 = st.columns(4)
    col_me0.metric(
        label="嘉兴地区（含海盐/平湖）",
        value=str(int(df[quarter_today].iloc[17]*100))+" %",
        delta=str(int(df[month_today].iloc[17]*100))+" %",
        )
    col_me1.metric(
        label="嘉兴/海宁/桐乡",
        value=str(int(df[quarter_today].iloc[2]*100))+" %",
        delta=str(int(df[month_today].iloc[2]*100))+" %",
        )
    col_me2.metric(
        label="平湖",
        value=str(int(df[quarter_today].iloc[12]*100))+" %",
        delta=str(int(df[month_today].iloc[12]*100))+" %",
        )
    col_me3.metric(
        label="海盐",
        value=str(int(df[quarter_today].iloc[7]*100))+" %",
        delta=str(int(df[month_today].iloc[7]*100))+" %",)
    st.dataframe(df)
def kdz_data():
    # 客单数据
    st.header("客单值及配套率")
    st.write("数据日期：2023年1月1日-2023年5月31日")
    df_kdz = pd.read_excel("KDZ.xlsx",index_col=0)
    df_kdz = df_kdz.set_index("门店")
    col_kdz1,col_kdz2 = st.columns(2)
    with col_kdz1:
        st.bar_chart(df_kdz["配套率."])
    with col_kdz2:
        st.bar_chart(df_kdz["客单值/万"])
    st.dataframe(df_kdz.iloc[:,:-1])

with st.sidebar:
    choose = st.sidebar.selectbox(
        "选择事项",
        ("出货数据","客单值及配套率","文件检索"))
if choose == "客单值及配套率":
    secret_run = '1919'
    secret_input = st.text_input("请输入密码：")
    if len(secret_run) > 0 and secret_input == st.secrets["Secrets"]["kdz_secret"]:
        st.success("密码正确！", icon="✅")
        kdz_data()
    else:
        st.error("请输入或更正密码！", icon="🚨")
elif choose == "出货数据":
    secret_run = "1919"
    secret_input = st.text_input("请输入密码：")
    if len(secret_run) > 0 and secret_input == st.secrets["Secrets"]["ch_secret"]:
        st.success("密码正确！", icon="✅")
        ch_data()
    else:
        st.error("请输入或更正密码！", icon="🚨")
