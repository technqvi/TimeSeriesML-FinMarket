#!/usr/bin/env python
# coding: utf-8

# In[245]:


import pandas as pd
import numpy as np
import os
from datetime import datetime,date,timedelta

import yfinance as yf

from ta.utils import dropna
import ta.trend as ta_trend
import ta.momentum as ta_mmt
import ta.others as ta_other
import ta 

# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import seaborn as sns



from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from google.api_core.exceptions import BadRequest

# Often when people are talking about the stock market, 
# they're referring to US exchanges – such as the NYSE or NASDAQ – which are open from 14.30 to 21:00 (UTC)


# In[ ]:


import functions_framework
@functions_framework.http
def load_asset_price_yahoo(request):


# # Enviroment Variable 

# In[255]:


    start_date=os.environ.get('START_DATE', '')  # First recoud 
    end_date=os.environ.get('END_DATE', '') 
    #symbol_str_list="SPY,QQQ,ACWI"
    symbol_str_list=os.environ.get('SYMBOL_STR_LIST', 'SPY') 
    nLastToIndy=int(os.environ.get('N_LAST_DATA', '45'))  # default=45


    # # Constant Value

    # In[247]:


    source='yahoo'  # csv / yahoo
    #write_method='WRITE_EMPTY' #'WRITE_TRUNCATE'
    write_method='WRITE_APPEND'


    # In[248]:


    symbol_list= symbol_str_list.split(',')
    import_dt=datetime.now()
    if  start_date=='' and end_date=='':
      start_date=(import_dt+timedelta(days=-1)).strftime("%Y-%m-%d")
      end_date= import_dt.strftime("%Y-%m-%d")

    print(f"Get {symbol_list} from {start_date} to {end_date} at {import_dt}" ) 


    # In[249]:


    list_cols=['Date','Symbol','Close']


    # # BigQuery

    # In[250]:


    projectId="pongthorn"
    dataset_id='FinAssetForecast'
    table_data_id=f"{projectId}.{dataset_id}.fin_data"
    print(table_data_id)

    client = bigquery.Client(project=projectId )

    def load_data_bq(sql:str):
     query_result=client.query(sql)
     df=query_result.to_dataframe()
     return df


    def importDataToBQ(dfToBQ):
        try:
                job_config = bigquery.LoadJobConfig(
                    write_disposition=write_method,
                )
                job = client.load_table_from_dataframe(
                    dfToBQ, table_data_id, job_config=job_config,
                )  # Make an API request.
                job.result()  # Wait for the job to complete.
                print(f"{source}-Total", len(dfToBQ), f" Add transaction to {table_data_id} bigquery successfully")
        except:
              print(job.error_result)


    # # Build Indicator as Feature using TA-Lib

    # In[251]:


    def build_indicator_feature(df):
        #df['MA5']=ta_trend.sma_indicator(close=df['Close'],window=5,fillna=True).round(4)
        df['EMA1']=ta_trend.ema_indicator(close=df['Close'],window=10,fillna=True).round(4)
        df['EMA2']=ta_trend.ema_indicator(close=df['Close'],window=20,fillna=True).round(4)
        df['MACD']=ta_trend.macd(close=df['Close'], window_slow=20, window_fast=10, fillna=True).round(4)
        df['SIGNAL']=ta_trend.macd_signal(close=df['Close'], window_slow=20, window_fast=10,window_sign=15, fillna=True).round(4)
        return df   


    # # Load data from CSV (Export from Amibroker)

    # In[252]:


    if source=='csv':
        print("Load data from CSV (Export from Amibroker)")
        '''
        Afl file on Amibroker  Explore to train TS 01-12-2014 - 31-05-2023
        Filter=1; 
        AddColumn(C,"close"); 
        '''
        ab_path="data/AB-SPY_2014-12-01-2023-05-31.csv"
        dfCSV=pd.read_csv(f'{ab_path}',parse_dates=['Date/Time'],dayfirst=True)
        dfCSV.columns=['Symbol','Date','Close']
        dfCSV=dfCSV[list_cols]
        dfCSV=dfCSV.drop_duplicates(subset=['Date','Symbol'],keep='last')
        dfCSV=build_indicator_feature(dfCSV)
        dfCSV['ImportDateTime']=import_dt
        print(dfCSV.info())
        importDataToBQ(dfCSV)


    # # Load data from Yahoo

    # In[253]:


    if source=='yahoo':
        print("Load data from Yahoo")
        dfMain=pd.DataFrame(columns=list_cols)
        print(dfMain)

        for symbol in symbol_list:

            dfx=yf.download(tickers=symbol,start=start_date,end=end_date)

            if dfx.empty==False:
                print(f"=============={symbol}=============")  
                dfx.reset_index(drop=False,inplace=True)  
                dfx['Symbol']=symbol
                dfx=dfx[['Date','Symbol','Close']] 

                minDate=dfx['Date'].min().strftime("%Y-%m-%d")
                print("First Row of Yahoo"+minDate)
                sqlX=f"""
                SELECT Date,Symbol,Close FROM `{table_data_id}` 
                Where  Date between  DATE_SUB(DATE '{minDate}', INTERVAL {nLastToIndy} Day) and '{minDate}' 
                and Symbol='{symbol}' order by Date,ImportDateTime
                """
                dfHist=load_data_bq(sqlX)


                dfx=pd.concat([dfHist,dfx],axis=0,ignore_index=True)

                print(f"No {len(dfx)} past data+current to calculate TA-Indicator")
                dfx=dfx.drop_duplicates(subset=['Date','Symbol'],keep='last')
                dfx['Date']=pd.to_datetime(dfx['Date'],format='%Y-%m-%d')

                dfx=build_indicator_feature(dfx)


                print(dfx.info())            

                #dfx=dfx[dfx.Date.between(start_date, end_date)]
                dfx = dfx.query('Date >= @start_date and Date < @end_date')

                print(dfx)
                dfMain=pd.concat([dfMain,dfx])


            else:
              msg=f"Not found {symbol} OR No data between {start_date} and {end_date}"
              print(msg)
              #return  msg
        if dfMain.empty==False:
            dfMain['ImportDateTime']=import_dt
            print(dfMain.info())
            #dfMain
            importDataToBQ(dfMain)


    # In[ ]:


    return 'OK'

