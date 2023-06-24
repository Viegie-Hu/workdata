#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import datetime

class XsData():
    """docstring for ClassName"""
    def __init__(self, filepath):
        self.filepath = filepath
    def Dfdata(self,startdate,enddate):
        df = pd.read_csv(self.filepath,encoding="utf-8")
        df1_ = df[["单据日期","门店","数量",'金额']][df['金额']!=0]
        df1_ = df1_.fillna(0)
        df1_ = df1_.replace(np.nan,0)
        df1_['单据日期'] = pd.to_datetime(df1_['单据日期'])
        df1_ = df1_[(df1_["单据日期"].dt.date >= startdate) & (df1_["单据日期"].dt.date <= enddate)]
        return df1_
        pass
    def Df(self,df,a="金额"):
        df1 = df1_[["单据日期","门店",a]]
        df1 = df1.groupby([df1["门店"],df1["单据日期"].apply(lambda x:x.month)]).sum()
        alist = df1.index.get_level_values(0).drop_duplicates()
        if a == "金额":
            df2 = pd.DataFrame({"门店":alist,"平均值":[round(int(df1.loc[i].mean())/10000,2) for i in alist],
                                "中位数":[round(int(df1.loc[i].median())/10000,2) for i in alist],
                                "标准差":[round(int(np.array(df1.loc[i]).std())/10000,2) for i in alist],
                                "Q1":[round(int(df1.loc[i].quantile(0.25))/10000,2) for i in alist],
                                "Q3":[round(int(df1.loc[i].quantile(0.75))/10000,2) for i in alist],
                                "最大值":[round(int(df1.loc[i].max())/10000,2) for i in alist],
                                "最小值":[round(int(df1.loc[i].min())/10000,2) for i in alist],
                                "合计":[round(int(df1.loc[i].sum())/10000,2) for i in alist]})
        elif a == "数量":
            df2 = pd.DataFrame({"门店":alist,"平均值":[int(df1.loc[i].mean()) for i in alist],
                                "中位数":[int(df1.loc[i].median()) for i in alist],
                                "标准差":[int(np.array(df1.loc[i]).std()) for i in alist],"Q1":[int(df1.loc[i].quantile(0.25)) for i in alist],
                                "Q3":[int(df1.loc[i].quantile(0.75)) for i in alist],"最大值":[int(df1.loc[i].max()) for i in alist],
                                "最小值":[int(df1.loc[i].min()) for i in alist],"合计":[int(df1.loc[i].sum()) for i in alist]})
        else:
            pass
        return df2
