import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'
#plt.rcParams['font.sans-serif']=['SimHei'] #显示中文
import datetime
import seaborn as sns
rc = {'font.sans-serif': 'SimHei',
      'axes.unicode_minus': False}
sns.set(style='darkgrid',rc=rc)
daytime = datetime.date.today()

class Daydata():
	"""docstring for Daydata"""
	def __init__(self,daydata_filename):
		self.daydata_filename = daydata_filename
	def ta_data(self):
	    df = pd.read_csv(self.daydata_filename,encoding='utf-8')
	    df_cy = df.iloc[:,14:-1]#创建df副本
	    df_cy.columns = ['门店',"销售","接待","电销","留资（电话）",
	    "加微","集赞","派函","开单","销售额","今日总结","明日计划"]
	    df_cy['时间'] = pd.to_datetime(df['开始答题时间']).dt.date
	    df_cy['时间'] = pd.to_datetime(df_cy['时间'])
	    df_cy['时间2'] = daytime.today()
	    df_today = df_cy[df_cy['时间']==df_cy['时间2']].iloc[:,:-1].sort_values('销售额',ascending=False)
	    df_all = pd.pivot_table(df_cy,index = ['门店','销售'],values=['接待','电销','留资（电话）',
	        '加微','集赞','派函','开单','销售额'],
	        aggfunc='sum').sort_values('销售额',ascending=False).reset_index()
	    return df_today,df_all
	def draw_ta(self,df_ta,ind_name="销售",col_name='销售额'):
	    #df_today,df_all = self.ta_data()
	    x = df_ta[ind_name]
	    y = df_ta[col_name]
	    fig,ax = plt.subplots()
	    plt.figure(dpi=500)
	    ax.barh(x,height=0.5,width=y,align="center",label=col_name)
	    for a,b in zip(x,y):
	        ax.text(b,a,b,ha='right',va='center',fontsize=12,color='w')
	    ax.legend()
	    return fig


