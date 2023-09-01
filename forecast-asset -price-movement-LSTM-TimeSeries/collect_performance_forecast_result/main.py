#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import os
from datetime import datetime,date,timedelta,timezone
import calendar
import json


from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from google.api_core.exceptions import BadRequest



# In[3]:



# uncomment and indent
import functions_framework
@functions_framework.http
def collect_prediction_result(request):   # run on clound function
# def collect_prediction_result(collectionDate):
    

    # # Init parameter
    mode=2 

    # In[4]:

    # uncoment
    modelList=['spy-ema1-60t10-ds0115t0523','qqq-ema1-30t5-ds0115t0523']


    if mode==1: # Migrate to backfill data and Test 
        logDate=collectionDate
        log_date=datetime.strptime(logDate,'%Y-%m-%d %H:%M')
        log_timestamp=datetime.strptime(logDate,'%Y-%m-%d %H:%M')
    else: # On weekly basis
        log_timestamp=datetime.now(timezone.utc)
        log_date=datetime.strptime(log_timestamp.strftime('%Y-%m-%d'),'%Y-%m-%d')

    week_day=log_date.weekday()
    day_name=calendar.day_name[log_date.weekday()]

    print(f"Date to collect data on {log_date.strftime('%Y-%m-%d')} {day_name}(Idx:{week_day}) at {log_timestamp}")

    if  week_day==5:
        last_trading_day_of_week=1
    elif week_day==6:
        last_trading_day_of_week=2
    else:
        raise Exception("Saturday OR Sunday,Both are allowed  as Collection Date for forcasting result.")   

    print(f"week_day={week_day} and last_trading_day_of_week={last_trading_day_of_week}")

    dictCollectPerf={}


    # In[ ]:





    # In[7]:


    genTableSchema=False
    metric_name='mae'

    # comment
    #model_id='spy-ema1-60t10-ds0115t0523'
    #model_id="spy-signal-60t10-ds0115t0523"
    #model_id='qqq-ema1-30t5-ds0115t0523'


    # # BigQuery Setting & Configuration Variable

    # In[8]:


    date_col='date'
    projectId='pongthorn'
    dataset_id='FinAssetForecast'

    table_data_id=f"{projectId}.{dataset_id}.fin_data"
    table_id = f"{projectId}.{dataset_id}.fin_movement_forecast"
    table_model_id= f"{projectId}.{dataset_id}.model_ts_metadata"

    table_perf_id= f"{projectId}.{dataset_id}.model_forecast_performance"

    print(table_id)
    print(table_data_id)
    print(table_model_id)
    print(table_perf_id)

    client = bigquery.Client(project=projectId )

    def load_data_bq(sql:str):
        query_result=client.query(sql)
        df=query_result.to_dataframe()
        return df


    # # Check where the given date collected data or not?

    # In[9]:


    sqlCheck=f"""
    select collection_timestamp from `{table_perf_id}`
    where date(collection_timestamp)='{log_date.strftime('%Y-%m-%d')}'
    """
    print(sqlCheck)
    dfCheckDate=load_data_bq(sqlCheck)
    if  dfCheckDate.empty==False:

        # uncomment
        return f"Collection data on {log_date} found, no any action"
    else:
        print(f"We are ready to Collect data on {log_date}")


    # # Create Start to End Date By Getting Last Date of Week

    # In[10]:


    # get  prev prediction  from  get end prediction to beginneg or predicton of week 
    endX=log_date+timedelta(days=-last_trading_day_of_week)
    startX=endX+timedelta(days=1)+timedelta(days=-5)
    print(f"Collection data from {startX.strftime('%A %d-%m-%Y')} to {endX.strftime('%A %d-%m-%Y')}")

    endX=endX.strftime('%Y-%m-%d')
    startX=startX.strftime('%Y-%m-%d')

    print(f"Convert start and end data {startX} - {endX} to string")


    # # Start Loop

    # In[11]:


    # uncomment  and indent
    def process_data(model_id):
        print(f"Collect data : {model_id} ")


        # # Get Model Meta

        # In[12]:


        def get_model_metadata(model_id):
            sqlModelMt=f"""
            SELECT * FROM `{table_model_id}`  where model_id='{model_id}'
            """
            print(sqlModelMt)
            dfModelMeta=load_data_bq(sqlModelMt)
            return  dfModelMeta

        dfModelMeta=get_model_metadata(model_id)

        if dfModelMeta.empty==False:
            modelMeta=dfModelMeta.iloc[0,:]
            print(modelMeta)
            asset_name=modelMeta['asset']
            prediction=modelMeta['prediction']
        else: 
            raise Exception(f"Not found model id  {model_id}")


        # # Retrive forecasting result data to Dictionary

        # In[13]:


        def get_forecasting_result_data(request):

            if   request is not None:  
                start_date=request["start_date"]
                end_date=request["end_date"]
                prediction_name=request["prediction_name"]
                asset_name=request["asset_name"]
                model_id=request["model_id"]
            else:
                raise Exception("No request parameters such as start_date,prediction_name,asset_name")

            print("1.How far back in time does model want to apply as input to make prediction")

            sqlInput=f"""
            select t.prediction_date,t.pred_timestamp,t.asset_name,t.prediction_name,
            t_feature.input_date as {date_col},t_feature.input_feature as {prediction_name}
            from  `{table_id}` t
            cross join unnest(t.feature_for_prediction) t_feature
            where (t.prediction_date>='{start_date}' and  t.prediction_date<='{end_date}')
            and t.model_id='{model_id}'
            order by  t.prediction_date,t_feature.input_date
            """
            print(sqlInput)
            dfInput=load_data_bq(sqlInput)
            # dfInput=dfInput.drop_duplicates(subset=[date_col,'asset_name','prediction_name'],keep='last',)
            # dfInput=dfInput.drop_duplicates(subset=[date_col],keep='last',)
            dfInput[date_col]=pd.to_datetime(dfInput[date_col],format='%Y-%m-%d')
            dfInput.set_index(date_col,inplace=True)

            input_sequence_length=len(dfInput)
            print(f"input_sequence_length={input_sequence_length}")
            

            print(dfInput.info())
            print(dfInput[['prediction_date','asset_name','prediction_name' ,prediction_name]])
            print("================================================================================================")
            
            print("2.How far in advance does model want to  make prediction")
            sqlOutput=f"""
            select t.prediction_date, t.pred_timestamp,t.asset_name,t.prediction_name,
            t_pred.output_date as {date_col},t_pred.output_value as {prediction_name}
            from  `pongthorn.FinAssetForecast.fin_movement_forecast` t
            cross join unnest(t.prediction_result) t_pred
            where (t.prediction_date>='{start_date}' and  t.prediction_date<='{end_date}')
            and t.model_id='{model_id}'
            order by  t.prediction_date,t_pred.output_date
            """
            print(sqlOutput)
            dfOutput=load_data_bq(sqlOutput)
            # dfOutput=dfOutput.drop_duplicates(subset=[date_col,'asset_name','prediction_name'],keep='last',)
            # dfOutput=dfOutput.drop_duplicates(subset=[date_col],keep='last',)
            dfOutput[date_col]=pd.to_datetime(dfOutput[date_col],format='%Y-%m-%d')
            dfOutput.set_index(date_col,inplace=True)

            output_sequence_length=len(dfOutput)
            print(f"output_sequence_length={output_sequence_length}")
            

            print(dfOutput.info())
            print(dfOutput[['prediction_date','asset_name','prediction_name' ,prediction_name]])
            print("================================================================================================")

            
            #get actual data since the fist day of input and the last day of output(if covered)
            startFinData=dfInput.index.min().strftime('%Y-%m-%d')
            endFindData=dfOutput.index.max().strftime('%Y-%m-%d')
            print(f"3.Get Real Data  to compare to prediction from {startFinData} to {endFindData}")

            sqlData=f"""
            select Date as {date_col},{prediction_name}, ImportDateTime, from `{table_data_id}` 
            where (Date>='{startFinData}' and Date<='{endFindData}') and Symbol='{asset_name}'
            order by ImportDateTime,Date
            """
            print(sqlData)

            dfRealData=load_data_bq(sqlData)
            dfRealData=dfRealData.drop_duplicates(subset=[date_col],keep='last',)
            dfRealData[date_col]=pd.to_datetime(dfRealData[date_col],format='%Y-%m-%d')
            dfRealData.set_index(date_col,inplace=True)
            
            print(dfRealData.info())
            print(dfRealData[[prediction_name]])
            print("================================================================================================")

            return {'actual_price':dfRealData,'input':dfInput,'output':dfOutput }


        print(f"================Get data from {startX}====to==={endX}================")
        request={'start_date':startX,'end_date':endX,'prediction_name':prediction,'asset_name':asset_name,'model_id':model_id}
        data=get_forecasting_result_data(request)
        print(f"=======================================================================")


        # # Create Predictive and Actual Value dataframe

        # In[14]:


        myTradingDataList=data['output']['prediction_date'].unique()
        print(myTradingDataList)


        # In[15]:


        dfAllForecastResult=pd.DataFrame(columns=['date','pred_value','actual_value','prediction_date'])

        print(f"========================Actual Price========================")
        dfX=data['actual_price'][[prediction]]
        dfX.columns=[f'actual_value']
        # print(dfX)

        # actually , we can jon without spilting data by prediction_dtate
        for date in  myTradingDataList: # trading day on giver week
            print(f"========================={date}=========================")
            dfPred=data['output'].query("prediction_date==@date")[[prediction]]
            dfPred.columns=[f'pred_value']
            # print(dfPred)

            dfCompare=pd.merge(left=dfPred,right=dfX,how='inner',right_index=True,left_index=True)
            dfCompare.reset_index(inplace=True)   
            dfCompare['prediction_date']=date.strftime('%Y-%m-%d')      
            print(dfCompare) 
            # print(dfCompare.info())

            dfAllForecastResult= pd.concat([dfAllForecastResult,dfCompare],ignore_index=True)
            
            
        print("========================All values dataframe========================")
        print(dfAllForecastResult.info())
        print(dfAllForecastResult)


        # # Calculate Metric

        # ## Get sum distance between pred and actul value from prev rows

        # In[16]:


        sqlMetric=f"""
        with pred_actual_by_model as  
        (
        SELECT  detail.actual_value,detail.pred_value
        from `pongthorn.FinAssetForecast.model_forecast_performance`  t
        cross join unnest(t.pred_actual_data) as detail
        where t.model_id='{model_id}' and t.collection_timestamp<'{log_timestamp}'
        )
        select COALESCE( sum(abs(x.actual_value-x.pred_value)),0) as pred_diff_actual,count(*) as no_row  from pred_actual_by_model  x


        """

        if genTableSchema==False:
            print(sqlMetric)

            dfMetric=load_data_bq(sqlMetric)
            prevSum=dfMetric.iloc[0,0]
            prevCount=dfMetric.iloc[0,1]

        else:
        # for generating table schema
            prevSum=0
            prevCount=0

        print(f"Prev Sum={prevSum} and Count={prevCount}")


        # ## Cal sum distance between pred and actul value from last rows

        # In[17]:


        dfAllForecastResult['pred_diff_actual']=dfAllForecastResult.apply(lambda x : abs(x['pred_value']-x['actual_value']),axis=1)
        recentSum=dfAllForecastResult['pred_diff_actual'].sum()
        recentCount=len(dfAllForecastResult)

        dfAllForecastResult=dfAllForecastResult.drop(columns=['pred_diff_actual'])
        print(f"Recent Sum={recentSum} and Count={recentCount}")

        #https://en.wikipedia.org/wiki/Mean_absolute_error
        metric_value= round((prevSum+recentSum)/(prevCount+recentCount),2)
        print(f"{metric_name} = {metric_value}")


        # # Create Collection Performance Info Dataframe and Store 
        # 

        # In[18]:


        df=pd.DataFrame(data=[ [log_date,model_id,metric_name,metric_value,log_timestamp] ],
                        columns=["collection_date","model_id","metric_name","metric_value","collection_timestamp"])
        print(df.info())
        print(df)


        # In[19]:


        dictCollectPerf[model_id]=(df,dfAllForecastResult)


        # In[20]:


        # uncomment
        return f"gather data of {model_id}"


    # # End Loop

    # In[21]:


    # Iterate over model list
    # uncomment


    # In[24]:



    for modelID in modelList:
    # indent
      print(process_data(modelID))
      print("#########################################################")


    # In[ ]:





    # # Create Json Data 

    # In[25]:


    jsonDataList=[]
    for model_id,dataTuple in  dictCollectPerf.items():
        print(model_id)
        
        masterDF=dataTuple[0]
        masterDF["collection_date"]=masterDF["collection_date"].dt.strftime('%Y-%m-%d')
        masterDF["collection_timestamp"]=masterDF["collection_timestamp"].dt.strftime('%Y-%m-%d %H:%M:%S')
        master_perf = json.loads(masterDF.to_json(orient = 'records'))[0] # 1 main dataframe has 1 records
        
        detailDF=dataTuple[1]  
        # print(detailDF.info())
        
        #detailDF["prediction_date"]=detailDF["prediction_date"].dt.strftime('%Y-%m-%d')
        detailDF["date"]=detailDF["date"].dt.strftime('%Y-%m-%d')
        
        detail_perf= json.loads(detailDF.to_json(orient = 'records'))
        master_perf["pred_actual_data"]=detail_perf
        
        jsonDataList.append(master_perf)
        
    # with open("fin_forecast_performance.json", "w") as outfile:
    #     json.dump( jsonDataList, outfile)


    # In[ ]:





    # # Ingest Data to BigQuery

    # ## Try to ingest data to get correct schema and copy the schema to create table including partion/cluster manually

    # In[26]:


    try:
        table=client.get_table(table_perf_id)
        print("Table {} already exists.".format(table_id))
        # print(table.schema)
    except Exception as ex :
        print(str(ex))
        
    job_config = bigquery.LoadJobConfig()

    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    # Try to ingest data to get correct schema and copy the schema to create table including partiion/cluster manually
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND 


    job = client.load_table_from_json(jsonDataList,table_perf_id, job_config = job_config)
    if job.errors is not None:
        print(job.error_result)
        print(job.errors)
        # uncomment
        return "Error to load data to BigQuery"
    else:
        print(f"Import to bigquery successfully  {len(jsonDataList)} records")
        
    #job_config.schema
    # truncate table`pongthorn.FinAssetForecast.model_forecast_performance` 


    # In[27]:


    # uncomment
    return 'completely'


    # In[ ]:





# In[28]:


# uncomment
# Main 
# print("Collect prediction result to monitor performance model")

# # listLogDate=['2023-06-03 00:00','2023-06-10 00:00','2023-06-17 00:00','2023-06-24 00:00'] 
# # listLogDate=['2023-07-01 00:00','2023-07-08 00:00','2023-07-15 00:00','2023-07-22 00:00','2023-07-29 00:00'] 
# # listLogDate=['2023-08-05 00:00','2023-08-12 00:00','2023-08-19 00:00','2023-08-26 00:00']
# for  d in listLogDate:
#   print(collect_prediction_result(d))
#   print("************************************************************************************************")
        


# In[ ]:




