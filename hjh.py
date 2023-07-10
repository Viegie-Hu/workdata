import pandas as pd
import numpy as np
import datetime
'''
import matplotlib.pyplot as plt
%matplotlib inline
%config InlineBackend.figure_format = 'svg'
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文
import seaborn as sns
rc = {'font.sans-serif': 'SimHei',
      'axes.unicode_minus': False}
sns.set(style='darkgrid',rc=rc)
daytime = datetime.date.today()
'''
class KP():
    def __init__(self,filename):
        self.filename = filename
    def df_2(self):
        df = pd.read_csv(self.filename)
        df1 = df[['单据日期', '门店','商品','分类','数量','金额']][df['金额'] != 0]
        df2 = df1[(df1['分类']=='床垫') | (df1['分类']=='床架')]
        df2['单据日期'] = pd.to_datetime(df2['单据日期'])
        df2['单据日期'] = df2['单据日期'].dt.date
        return df2
    def df_pm(self,df2,pm='床垫'):
        df3 = df2[df2['分类'] == pm].groupby('商品').aggregate({'数量':'sum','金额':'sum'})
        df3 = df3.sort_values(by=['数量'],ascending=False)
        df3['金额'] = round(df3['金额']/10000,2)
        df3.columns = ['数量/张','金额/万']
        df3 = df3.head(20)
        return df3
    def df_5(self,df2):
        df5 = df2.groupby('分类').aggregate({"数量":"sum","金额":"sum"})
        df5['金额'] = round(df5['金额']/10000,2)
        df5_cj_num = df5.loc['床架','数量']
        df5_cd_num = df5.loc['床垫','数量']
        df5_cj_p = df5.loc['床架','金额']
        df5_cd_p = df5.loc['床垫','金额']
        df5_2 = pd.DataFrame({'地区':"杭嘉湖地区","床架数量/张":df5_cj_num,"床垫数量/张":df5_cd_num,"床架金额/万":df5_cj_p,
                              "床垫金额/万":df5_cd_p,'配套率':str(round(df5_cj_num/df5_cd_num*100))+"%",
                              '客单值/万':round((df5_cj_p+df5_cd_p)/(df5_cj_num+df5_cd_num),2)},index=[0])
        df5_2 = df5_2.set_index('地区')
        return df5_2
    def df_7(self,df2):
        df6 = df2.groupby(['门店','分类']).aggregate({"数量":"sum","金额":"sum"})
        df6['金额'] = round(df6['金额']/10000,2)
        df7_index = df6.index.get_level_values(0).drop_duplicates()
        cd_num,cj_num,cd_p,cj_p = [],[],[],[]
        for i in df7_index:
            if (i,'床垫') in df6.index:
                cd_num.append(df6.loc[(i,'床垫'),'数量'])
                cd_p.append(df6.loc[(i,'床垫'),'金额'])
            else:
                cd_num.append(0)
                cd_p.append(0)
            if (i,'床架') in df6.index:
                cj_num.append(df6.loc[(i,'床架'),'数量'])
                cj_p.append(df6.loc[(i,'床架'),'金额'])
            else:
                cj_num.append(0)
                cj_p.append(0)
            pass
        df7 = pd.DataFrame({'门店':df7_index,'床架数量':cj_num,"床垫数量":cd_num,"床架金额/万":cj_p,"床垫金额/万":cd_p})
        ptl = df7['床架数量']/df7['床垫数量']*100
        ptl = ptl.astype('int')
        df7['配套率'] = [str(i)+"%" for i in ptl]
        df7['客单值'] = round((df7['床架金额/万']+df7['床垫金额/万'])/(df7['床架数量']+df7['床垫数量']),2)
        df7['配套率.'] = round(df7['床架数量']/df7['床垫数量'],2)
        return df7
    def df_8(self,df2,dateone,datetwo):
        start_date = dateone
        end_date = datetwo
        df8 = df2[(df2['单据日期'] >= start_date)&(df2['单据日期'] <= end_date)]
        return df8
        