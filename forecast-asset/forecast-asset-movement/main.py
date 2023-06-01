#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np
import os
from datetime import datetime,date,timedelta,timezone
import pytz
import json

# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import seaborn as sns

from tensorflow.keras.models import load_model
import joblib

from google.cloud import storage
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from google.api_core.exceptions import BadRequest


# In[53]:


import functions_framework
@functions_framework.http
def forecast_asset_movement(request):


    # # Parameter

    # In[77]:


    #name = request.args.get("today", "today")
    #https://stackoverflow.com/questions/61573102/calling-a-google-cloud-function-from-within-python
    #https://medium.com/google-cloud/setup-and-invoke-cloud-functions-using-python-e801a8633096
    print("JSON Info") # Post Method
    request_json = request.get_json()
    print(request_json)

    # print(f"TODAY Request :{request_json['TODAY']}")
    # print(f"ASSET Request :{request_json['ASSET']}")
    # print(f"PREDICTION Request :{request_json['PREDICTION']}")
    print("==================================================")

    print("Value Info")
    print(request.values)

    print("Enviroment Variable")
    today=os.environ.get('TODAY', '') 
    #today=os.environ.get('TODAY', '2023-04-28')  
    asset_name=os.environ.get('ASSET', 'SPY')
    prediction_name=os.environ.get('PREDICTION','EMA1')
    print(f"{today} - {asset_name} -{prediction_name}")
    print("==================================================")

    loadModelMode='gcs'   # local,gcs


    # # Load model and scaler

    # In[78]:


    model_file="EMA1_60To10_SPY_E150S20-Y2015-2023_ma.h5"
    scaler_file="scaler_EMA1_60To10_SPY_E150S20-Y2015-2023.gz"
    scalerPred_file="scaler_pred_EMA1_60To10_SPY_E150S20-Y2015-2023.gz"

    if loadModelMode=='local':
     objectPaht="model/model-ema1"
    else:
     objectPaht="gs://demo-ts-forecast-pongthorn/model-ema1"   


    model_path=f"{objectPaht}/{model_file}"
    scale_input_path=f"{objectPaht}/{scaler_file}"
    scale_output_path=f"{objectPaht}/{scalerPred_file}"

    print(f"load model from {loadModelMode}")   
    print(model_path)
    print(scale_input_path)
    print(scale_output_path)



    # In[79]:


    if loadModelMode=='local':
        try:
            print("Model and Scaler Object Summary")
            x_model = load_model(model_path)
        except Exception as ex:
            print(str(ex))
            raise Exception(str(ex)) 

        try:
            print("Scaler Max-Min")
            x_scaler = joblib.load(scale_input_path)
            x_scalerPred=joblib.load(scale_output_path)

        except Exception as ex:
            print(str(ex))
            raise Exception(str(ex))

        print("=====================================================================================================")


    # In[80]:


    if loadModelMode=='gcs':
     try:    
        gcs_client = storage.Client()

        with open(scaler_file, 'wb') as scaler_f, open(scalerPred_file, 'wb') as scaler_pred_f,open(model_file, 'wb') as model_f:
            gcs_client.download_blob_to_file(scale_input_path, scaler_f
            )
            gcs_client.download_blob_to_file(scale_output_path, scaler_pred_f
            )
            gcs_client.download_blob_to_file(model_path, model_f
            )

        x_scaler = joblib.load(scaler_file)
        x_scalerPred=joblib.load(scalerPred_file)
        x_model = load_model(model_file)
     except Exception as ex:
        print(str(ex))
        raise Exception(str(ex))


    # In[81]:


    print(x_model.summary())
    #(max - min) / (X.max(axis=0) - X.min(axis=0))
    print(f"max={x_scaler.data_max_} and min={x_scaler.data_min_} and scale={x_scaler.scale_}")
    print(f"max={x_scalerPred.data_max_} and min={x_scalerPred.data_min_} and scale={x_scalerPred.scale_}")


    # # Declare and Initialize Variable

    # In[82]:


    date_col='Date'
    prediction_col=prediction_name
    feature_cols=[prediction_name]

    input_sequence_length =60
    output_sequence_length =10

    nLastData=input_sequence_length*2

    colInput='feature'
    colOutput='prediction'


    # dt_imported=datetime.now()
    dt_imported=datetime.now(timezone.utc)
    dtStr_imported=dt_imported.strftime("%Y-%m-%d %H:%M:%S")
    print(dtStr_imported)


    # # BigQuery Setting

    # In[83]:


    projectId='pongthorn'
    dataset_id='FinAssetForecast'
    table_id = f"{projectId}.{dataset_id}.fin_movement_forecast"
    table_data_id = f"{projectId}.{dataset_id}.fin_data"

    print(table_id)
    print(table_data_id)

    # json_credential_file=r'C:\Windows\pongthorn-5decdc5124f5.json'
    # credentials = service_account.Credentials.from_service_account_file(json_credential_file)
    # client = bigquery.Client(project=projectId,credentials=credentials )
    client = bigquery.Client(project=projectId )

    def load_data_bq(sql:str):
     query_result=client.query(sql)
     df=query_result.to_dataframe()
     return df


    # # Query Fin Data from BQ

    # In[84]:


    if today=='':
        sqlLastDate=f""" select max(Date) as LastDate  from `{table_data_id}` where Symbol='{asset_name}' """
        results = client.query(sqlLastDate)

        for row in results:
            lastDate=row['LastDate']    
            if  lastDate == None:
             raise Exception(f"Not found price data  of {asset_name}")
            lastDate=lastDate.strftime('%Y-%m-%d')


        today=lastDate
        print(f"Last Price of  {asset_name} at {today}")


    # In[85]:


    print(f"Get last price of {asset_name}")
    sqlLastPred=f"""select prediction_date,asset_name,prediction_name,pred_timestamp from `{table_id}` 
    where prediction_date='{today}' and   asset_name='{asset_name}'
    order by pred_timestamp 
    """
    print(sqlLastPred)
    dfLastPred=load_data_bq(sqlLastPred)
    if dfLastPred.empty==False:
       dfLastPred=dfLastPred.drop_duplicates(subset=['prediction_date','asset_name','prediction_name'],keep='last') 
       print(f"{asset_name}-{prediction_col}-{today} has been predicted price movement")
       print(dfLastPred)
       return "there is one record of prediction price movement."
    else:
       print(f"{asset_name}-{prediction_col} at {today} has not been predicted price movement yet.") 


    # In[86]:


    dayAgo=datetime.strptime(today,'%Y-%m-%d') +timedelta(days=-nLastData)
    print(f"Get data from {dayAgo.strftime('%Y-%m-%d')} - {today} as input to forecast")


    # In[87]:


    sql=f"""
    SELECT  *  FROM `{table_data_id}`  
    Where  {date_col} between  DATE_SUB(DATE '{today}', INTERVAL {nLastData} DAY) 
    and '{today}' and Symbol='{asset_name}' order by {date_col},ImportDateTime
    """
    print(sql)
    query_result=client.query(sql)
    df=query_result.to_dataframe()

    df=df.drop_duplicates(subset=[date_col,'Symbol'],keep='last')
    df[date_col]=pd.to_datetime(df[date_col],format='%Y-%m-%d')
    df.set_index(date_col,inplace=True)

    print(df.info())

    print(df[['Symbol','Close' ,'ImportDateTime']].head())
    print(df[['Symbol','Close' ,'ImportDateTime']].tail())

    if df.empty==True or len(df)<input_sequence_length:
        print(f"There is enough data to make prediction during {dayAgo.strftime('%Y-%m-%d')} - {today}")
        return "no enough data."


    # In[88]:


    # plt.subplots(2, 1, figsize = (20, 10),sharex=True)

    # ax1 = plt.subplot(2, 1, 1)
    # plt.plot(df[['Close','EMA1','EMA2']])
    # plt.ylabel('Price & EMA')

    # ax2 = plt.subplot(2, 1, 2)
    # plt.plot(df[['MACD','SIGNAL']])
    # plt.xlabel('Date')
    # plt.ylabel('MACD & Signal')

    # plt.show()


    # # Get only Feature( 1 Indicator) to Predict itself in the next N days

    # In[89]:


    print(f"Get Feature to Predict : {prediction_col} ")
    dfForPred=df[feature_cols]
    #dfForPred=dfForPred.iloc[-(input_sequence_length+1):-1,:]
    dfForPred=dfForPred.iloc[-input_sequence_length:,:]
    print(dfForPred.info())
    print(dfForPred.shape)

    print(dfForPred.head(5))
    print(dfForPred.tail(5))

    # dfForPred.plot(figsize = (20, 10))
    # plt.show()


    # # Make Pediction as Forecast

    # In[90]:


    xUnscaled=dfForPred.values #print(xUnscaled.shape)
    xScaled=x_scaler.transform(xUnscaled)
    print(xScaled.shape)
    print(xScaled[-5:])

    # # Way1
    # xScaledToPredict = []
    # xScaledToPredict.append(xScaled)
    # print(len(xScaledToPredict))

    # yPredScaled=x_model.predict(np.array(xScaledToPredict))
    # print(yPredScaled.shape,yPredScaled)

    # yPred  = x_scalerPred.inverse_transform(yPredScaled.reshape(-1, 1))
    # print(yPred.shape,yPred)

    #Way2
    xScaledToPredict= xScaled.reshape(1,input_sequence_length,len(feature_cols))
    print(xScaledToPredict.shape)

    yPredScaled = x_model.predict(xScaledToPredict)
    print(yPredScaled.shape, yPredScaled)

    yPred = x_scalerPred.inverse_transform(yPredScaled).reshape(-1, 1)
    print(yPred.shape, yPred)


    print("============================Summary============================")
    print(xUnscaled.shape)
    print(yPred.shape)

    # print("============================Input============================")
    # print(xUnscaled)
    # print("============================Output============================")
    # print(yPred)



    # # Build Predition Result Data

    # ## Feature Data

    # In[91]:


    dfFeature=pd.DataFrame(data= xUnscaled,columns=feature_cols,index=dfForPred.index)
    dfFeature['Type']=colInput
    print(dfFeature.shape)
    print(dfFeature.head())
    print(dfFeature.tail())


    # ## Forecast Value Data

    # In[92]:


    lastRowOfFeature=dfFeature.index.max()
    firstRowofPrediction=lastRowOfFeature+timedelta(days=1)
    datePred=pd.date_range(start=firstRowofPrediction,freq='b',periods=output_sequence_length)
    print(datePred)

    dfPrediction=pd.DataFrame(data= yPred,columns=feature_cols,index=datePred)
    dfPrediction.index.name=date_col
    dfPrediction['Type']=colOutput
    print(dfPrediction.shape)
    print(dfPrediction)


    # # Get Prepraed To ingest data into BQ , we have to create dataframe and convert to Json-Rowns

    # In[93]:


    outputDF=pd.DataFrame(data=[ [today,asset_name,prediction_col,dtStr_imported] ],columns=["prediction_date","asset_name","prediction_name","pred_timestamp"])
    print(outputDF.info())
    print(outputDF)


    # In[94]:


    jsonOutput = json.loads(outputDF.to_json(orient = 'records'))
    for item in jsonOutput:

        dataFeature=dfFeature.reset_index()[[date_col,prediction_col]]
        dataFeature[date_col]=dataFeature[date_col].dt.strftime('%Y-%m-%d')
        dataFeature.columns=["input_date","input_feature"]
        jsonFeature= json.loads(dataFeature.to_json(orient = 'records'))
        item["feature_for_prediction"]=jsonFeature

        dataPred=dfPrediction.reset_index()[[date_col,prediction_col]]
        dataPred[date_col]=dataPred[date_col].dt.strftime('%Y-%m-%d')
        dataPred.columns=["output_date","output_value"]
        jsonPred= json.loads(dataPred.to_json(orient = 'records'))
        item["prediction_result"]=jsonPred

    with open("fin_prediction.json", "w") as outfile:
        json.dump(jsonOutput, outfile)
    jsonOutput


    # # Ingest Data to BigQuery 

    # In[95]:


    try:
        table=client.get_table(table_id)
        print("Table {} already exists.".format(table_id))
        print(table.schema)
    except Exception as ex :
        print(str(ex))
    #if error  please create table and other configuration as  bq_prediction.txt    

    job_config = bigquery.LoadJobConfig(
    # schema=[  ]
    )

    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  
    #job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job = client.load_table_from_json(jsonOutput,table_id, job_config = job_config)
    if job.errors is not None:
        print(job.error_result)
        print(job.errors)
    else:
        print(f"import to bigquery successfully  {len(jsonOutput)} records")

    #job_config.schema


    # In[96]:


    return   'completed job.'


# In[ ]:





# In[97]:






