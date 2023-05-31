#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import numpy as np
import os
from datetime import datetime,date,timedelta
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

# how client call could function 
#https://www.geeksforgeeks.org/how-to-use-google-cloud-function-with-python/
#https://medium.com/google-cloud/setup-and-invoke-cloud-functions-using-python-e801a8633096
#https://codelabs.developers.google.com/codelabs/cloud-functions-python-http#6
#https://stackoverflow.com/questions/61573102/calling-a-google-cloud-function-from-within-python


# In[30]:


import functions_framework
@functions_framework.http
def forecast_asset_movement(request):

#name = request.args.get("today", "today")
# if   request is not None:  
#     today=request["today"]
#     asset_name=request["asset_name"]
#     prediction_name=request["prediction_name"]


# # Parameter

# In[31]:


    today='2023-04-28'
    asset_name="SPY"
    prediction_name='EMA1'
    loadModelMode='gcs'   # local,gcs


    # # Load model and scaler

    # In[32]:


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



    # In[ ]:





    # In[33]:


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


    # In[34]:


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


    # In[35]:


    print(x_model.summary())
    #(max - min) / (X.max(axis=0) - X.min(axis=0))
    print(f"max={x_scaler.data_max_} and min={x_scaler.data_min_} and scale={x_scaler.scale_}")
    print(f"max={x_scalerPred.data_max_} and min={x_scalerPred.data_min_} and scale={x_scalerPred.scale_}")


    # # Declare and Initialize Variable

    # In[36]:


    date_col='Date'
    prediction_col=prediction_name
    feature_cols=[prediction_name]

    input_sequence_length =60
    output_sequence_length =10

    nLastData=input_sequence_length*2

    colInput='feature'
    colOutput='prediction'


    dt_imported=datetime.now()
    dtStr_imported=dt_imported.strftime("%Y-%m-%d %H:%M:%S")
    print(dtStr_imported)


    # # BigQuery Setting

    # In[37]:


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


    # # Query Fin Data from BQ

    # In[38]:


    dayAgo=datetime.strptime(today,'%Y-%m-%d') +timedelta(days=-nLastData)
    print(f"Get data from {dayAgo.strftime('%Y-%m-%d')} - {today} as input to forecast")


    # In[39]:


    sql=f"""
    SELECT  *  FROM `{table_data_id}`  
    Where  {date_col} between  DATE_SUB(DATE '{today}', INTERVAL {nLastData} DAY) 
    and '{today}' and Symbol='{asset_name}' order by {date_col}
    """
    print(sql)
    query_result=client.query(sql)
    df=query_result.to_dataframe()

    df[date_col]=pd.to_datetime(df[date_col],format='%Y-%m-%d')
    df.set_index(date_col,inplace=True)

    print(df.info())

    print(df.head())
    print(df.tail())

    if df.empty==True or len(df)<input_sequence_length:
        print(f"There is enough data to make prediction during {dayAgo.strftime('%Y-%m-%d')} - {today}")
        return "no enough data"


    # In[40]:


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

    # In[41]:


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


    # # Make Pediction

    # In[42]:


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

    # In[43]:


    dfFeature=pd.DataFrame(data= xUnscaled,columns=feature_cols,index=dfForPred.index)
    dfFeature['Type']=colInput
    print(dfFeature.shape)
    print(dfFeature.head())
    print(dfFeature.tail())


    # ## Forecast Value Data

    # In[44]:


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

    # In[45]:


    outputDF=pd.DataFrame(data=[ [today,asset_name,prediction_col,dtStr_imported] ],columns=["prediction_date","asset_name","prediction_name","pred_timestamp"])
    print(outputDF.info())
    print(outputDF)


    # In[46]:


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

    # In[47]:


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


    # In[48]:


    return   'completed job.'


# In[ ]:





# In[49]:


# # indent method
# # uncomment both return statement

# if __name__ == "__main__":

# start_pred_date='2023-04-28'  # to make predictoin of 02 May 23
# table_date_id="pongthorn.FinAssetForecast.fin_data"
# asset_name='SPY'
# prediction_name='EMA1'

# projectId='pongthorn'
# json_credential_file=r'C:\Windows\pongthorn-5decdc5124f5.json'
# credentials = service_account.Credentials.from_service_account_file(json_credential_file)
# client = bigquery.Client(project=projectId,credentials=credentials )

# sqlXYZ=f"""
# SELECT  Date  FROM `{table_data_id}`  
# Where  Date >= '{start_pred_date}' and Symbol='{asset}' order by Date
# """
# print(sqlXYZ)
# query_result=client.query(sqlXYZ)
# dfXYZ=query_result.to_dataframe()

# for idx,row in dfXYZ.iterrows():
#     x_day=row["Date"]
#     request_data={"today":x_day.strftime('%Y-%m-%d'),"asset_name":asset_name,"prediction_name":prediction_name}
#     print(f"Predict data  with {request_data}")  
#     # result=forecast_asset_movement(request_data) 
#     # print(result)
#     print(f"========================================================================================================================")


# In[ ]:





# In[ ]:




