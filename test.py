import streamlit as st
import datetime
import pandas as pd
import math
import openpyxl
import time
from DayData import Daydata
import os
from hjh import KP
from XSdata import XsData
today = datetime.datetime.today()#获取日期
month_today = str(today.month)+'月'#获取月份
quarter_today = "Q"+str(math.ceil(today.month/3))#获取季度

def xs_data():
    st.header("销售数据公示")
    #name = os.path.abspath(r"C:\Users\D2652\Desktop\workdata\daydata.csv")
    a_today = Daydata("daydata.csv")
    df_today,df_all,df_xiaoshou,df_mendian=a_today.ta_data()
    #每日数据排名
    st.subheader("当日销售数据排名")
    st.text(str(today))
    col_data0,col_data1 = st.columns(2)
    with col_data0:
        indcol0 = st.selectbox(
            "请选择门店或销售：",
            ("销售",'门店'),
            key=0)
    with col_data1:
        indcol1 = st.selectbox(
            "请选择想要查看的项目：",
            ("销售额","接待","电销","留资（电话）","加微","集赞","派函","开单"),
            key=1)
    df_today = df_today.set_index(indcol0)
    st.bar_chart(df_today[indcol1])
    #st.pyplot(a_today.draw_ta(df_today))
    st.dataframe(df_today.iloc[:,:-1])
    st.divider()
    # 累计数据排名
    st.subheader("累计销售数据排名")
    col_data2,col_data3 = st.columns(2)
    with col_data2:
        indcol2 = st.selectbox(
            "请选择门店或销售：",
            ("销售",'门店',),
            key=2)
    with col_data3:
        indcol3 = st.selectbox(
            "请选择想要查看的项目：",
            ("销售额","接待","电销","留资（电话）","加微","集赞","派函","开单",),
            key=3)
    df_all = df_all.set_index(indcol2)
    st.bar_chart(df_all[indcol3])
    st.dataframe(df_all)
    st.divider()
    #数据趋势变化
    st.subheader("数据趋势变化")
    indcol4 = st.selectbox("请选择想要查看的项目：",
        ("销售额","接待","电销","留资（电话）","加微","集赞","派函","开单",),
        key=4)
    st.text("各销售"+indcol4+"数据趋势变化")
    st.line_chart(df_xiaoshou[indcol4])
    st.dataframe(df_xiaoshou[indcol4])
    st.text("各门店"+indcol4+"数据趋势变化")
    st.line_chart(df_mendian[indcol4])
    st.dataframe(df_mendian[indcol4])
def ch_data():
    # 出货数据
    st.header("出货数据")
    st.subheader(f"{quarter_today}及{month_today}出货完成率")
    df = pd.read_excel("CHdata.xlsx")
    df = df.loc[:,"嘉兴地区年度目标数据":]
    df.columns = df.iloc[0,:]
    df = df.set_index(["城市","项目"])
    df = df.fillna(0)
    df = df.iloc[2:,:].astype("float64")
    df = df.round(2)
    col_me00,col_me0 = st.columns(2)
    col_me00.metric(
        label="杭嘉湖地区",
        value=str(int(df[quarter_today].iloc[22]*100))+" %",
        delta=str(int(df[month_today].iloc[22]*100))+" %",
        )
    col_me0.metric(
        label="嘉兴地区（含海盐/平湖）",
        value=str(int(df[quarter_today].iloc[17]*100))+" %",
        delta=str(int(df[month_today].iloc[17]*100))+" %",
        )
    col_me1,col_me2,col_me3 = st.columns(3)
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
    st.dataframe(df.iloc[:26,:])

# 日常运行客单值和配套率数据，避免每次打开界面重新读取
hjh_kdz = KP('HJHsalesdata.csv')
df2 = hjh_kdz.df_2()
df7 = hjh_kdz.df_7(df2=df2).set_index('门店')
df8 = hjh_kdz.df_8(df2=df2)
df9 = hjh_kdz.df_7(df2=df8).set_index('门店')
with st.sidebar:
    choose = st.sidebar.selectbox(
        "选择事项",
        ("销售数据","出货数据","杭嘉湖客&配","嘉兴客&配","销售数据A"))

if choose == "销售数据":
    xs_data()
    pass
elif choose == "杭嘉湖客&配":
    secret_input = st.text_input("请输入密码：")
    if len(secret_input) > 0 and secret_input == st.secrets["Secrets"]["kdz_secret"]:
        st.success("密码正确！", icon="✅")
        st.header("杭嘉湖地区相关数据")
        hjh_kdz_col0,hjh_kdz_col1 = st.columns(2)
        with hjh_kdz_col0:
            st.subheader("杭嘉湖地区床垫销量前20榜单")
            st.dataframe(hjh_kdz.df_pm(df2=df2,pm="床垫"))
        with hjh_kdz_col1:
            st.subheader("杭嘉湖地区床架销量前20榜单")
            st.dataframe(hjh_kdz.df_pm(df2=df2,pm="床架"))
        st.divider()
        st.subheader("杭嘉湖地区客单值&配套率")
        st.dataframe(hjh_kdz.df_5(df2=df2))
        st.divider()
        st.subheader("杭嘉湖各门店客单值&配套率")
        st.write("数据自开业之日起")
        st.bar_chart(df7['配套率.'])
        st.bar_chart(df7['客单值'])
        st.dataframe(df7.iloc[:,:-1])
        st.divider()
        st.subheader("杭嘉湖各门店客单值&配套率")
        st.write("数据：2023年1月1日-2023年5月31日")
        st.bar_chart(df9['配套率.'])
        st.bar_chart(df9['客单值'])
        st.dataframe(df9.iloc[:,:-1])
    else:
        st.error("请输入或更正密码！", icon="🚨")
elif choose == "出货数据":
    secret_input = st.text_input("请输入密码：")
    if len(secret_input) > 0 and secret_input == st.secrets["Secrets"]["ch_secret"]:
        st.success("密码正确！", icon="✅")
        ch_data()
    else:
        st.error("请输入或更正密码！", icon="🚨")
