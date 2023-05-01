# %%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# %% [markdown]
# # Load and Transform Data

# %%
# data_path=r"D:\PythonDev\MyQuantFinProject\TimeSeriesML-FinMarket\data"
# file_path=os.path.join(data_path,'SPY_INDY_Y16.csv')
# result_path=os.path.join(data_path,'SPY_Trend_20-22.xlsx')

# colSumSince='Signal10_20_15'

# df=pd.read_csv(file_path,index_col='Date/Time',parse_dates=['Date/Time'],dayfirst=True)
# print(list(df.columns))
# df=df['2020':'2022']
# print(df.info())
# df.head()


# %%
def create_trend_feature(df,colSumSince):

# %%
  df=df.reset_index(drop=False)
  df_date=df[['Date/Time']]
  df=df[[colSumSince]]


  # %% [markdown]
  # # Sum and Count Trend

  # %%
  colUp=f'{colSumSince}_Up'
  colUpCount=f'{colSumSince}_UpCount'
  colDown=f'{colSumSince}_Down'
  colDownCount=f'{colSumSince}_DownCount'

  def find_sum_trend(lookback=1,trendID=1):  # 1=up 0=down
    sumsinceList=[]
    countList=[]
    sum_x=0
    for i in range(0, len(df)):
          if i<lookback:
              sumsinceList.append(0)
              countList.append(0)
          elif i>=lookback:
            logic= df.loc[i,colSumSince] > df.loc[i-lookback,colSumSince] if trendID==1 else df.loc[i,colSumSince] <= df.loc[i-lookback,colSumSince]
            if logic:
              sum_x=sum_x+1
              sumsinceList.append(sum_x)  
              countList.append(1)
            else:
              sum_x=0
              sumsinceList.append(0)   
              countList.append(0)  
    return sumsinceList,countList


  # %%
  sum_up,count_up= find_sum_trend(lookback=1,trendID=1)
  sumUpDF=pd.DataFrame ( {colUp:sum_up,colUpCount:count_up})

  sum_down,count_down=find_sum_trend(lookback=1,trendID=0)
  sumDownDF=pd.DataFrame ( {colDown:sum_down,colDownCount:count_down})

  df_x=pd.concat([df_date,df,sumUpDF,sumDownDF],axis=1)
  df_x.set_index('Date/Time',inplace=True)
  print(df_x.info())

  # df_x.to_csv("X.csv")

  # %%
  # df_x.plot(kind='line',layout=(len(df_x.columns),1),
  #                       sharex=True,subplots=True,figsize=(15, 3*len(df_x.columns)))
    
  # plt.show()

  # %% [markdown]
  # # Group Trend to find distrubution

  # %%
  df_x.reset_index(drop=False,inplace=True)
  df_x.rename(columns={"Date/Time":"Date"},inplace=True)

  # filter only uptrend to group count
  dfUp=df_x.query(f"{colUp}>0").reset_index(drop=True).loc[:,['Date',colUp]]

  # filter only downtrend to group count
  dfDown=df_x.query(f"{colDown}>0").reset_index(drop=True).loc[:,['Date',colDown]]


  # %%
  def group_trend(dfGroup,colTrend):  # Up=up Down=down
    groupList=[]
    group_name=''
    for i in range(0, len(dfGroup)):
      if i==0:
        group_name=dfGroup.loc[i,'Date'].strftime("%d%b%y")  
        groupList.append(group_name)  
      else:
        if dfGroup.loc[i,colTrend]> dfGroup.loc[i-1,colTrend]:
          groupList.append(group_name) 
        else:
          group_name=dfGroup.loc[i,'Date'].strftime("%d%b%y")  
          groupList.append(group_name)  
          
    return groupList


  # %%
  colGroupUp='Up'
  groupUp=group_trend(dfUp,colUp)
  dfUp=pd.concat([dfUp,pd.DataFrame({colGroupUp:groupUp})],axis=1)
  # print(dfUp.info())
  # print(dfUp)

  dfUpGroupX=dfUp.groupby([colGroupUp])[[colUp]].max()
  dfUpGroupX=dfUpGroupX.sort_values(by=colUp,ascending=False)
  # dfUpGroupX



  # %%
  colGroupDown='Down'
  groupDown=group_trend(dfDown,colDown)
  dfDown=pd.concat([dfDown,pd.DataFrame({colGroupDown:groupDown})],axis=1)
  # print(dfDown.info())
  # print(dfDown)

  dfDownGroupX=dfDown.groupby([colGroupDown])[[colDown]].max()
  dfDownGroupX=dfDownGroupX.sort_values(by=colDown,ascending=False)
  # dfDownGroupX

  # %%
  # fig,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(14,7))
  # dfUpGroupX.plot.hist(ax=ax1)
  # dfDownGroupX.plot.hist(ax=ax2)

  # %%
  return  df_x,dfUpGroupX,dfDownGroupX

# %%
# writer=pd.ExcelWriter(result_path,engine='xlsxwriter') 

# df_x.to_excel(writer, sheet_name="All-Trend",index=False)
# dfUp.to_excel(writer,sheet_name="UpTrend",index=False)
# dfUpGroupX.to_excel(writer,sheet_name="UpSummary",index=True)
# dfDown.to_excel(writer,sheet_name="DownTrend",index=False)
# dfDownGroupX.to_excel(writer,sheet_name="DownSummary",index=True)
# writer.save()

# %%


# %%



