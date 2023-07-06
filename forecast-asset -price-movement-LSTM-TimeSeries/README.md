# About
This is experimental project to guid you how to predict stock price movement pattern pattern with End to End Solution .
Load Data => Build Model ==> Forecast Model ==> Deploy Model ==> Visualize Forecasting Result.

## [Forecast Asset Future Price Movement By LSTM-TimeSeries](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries)
### [load_daily_price_from_yahoo.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset%20-price-movement-LSTM-TimeSeries/load_daily_price_from_yahoo.ipynb)
##### Youtube : [1 Load Stock Price From Yahoo To BigQuery For Building LSTM Model](https://www.youtube.com/watch?v=jaPpyopNFPA&feature=youtu.be)
* There are 2 options to load price data to GoogleBiquery.
* Option#1 Export data price from Amibroker as csv file and load it to bigquery.
* Option#2 Pull data price from [finance.yahoo.com](https://finance.yahoo.com/) by using [yfinance](https://github.com/ranaroussi/yfinance) as dataframe and load it to bigquery .
* To build any technical analysis indicator as features to get prepred for building Time-Series Machine Learning, we can appy [Technical Analysis Library in Python](https://technical-analysis-library-in-python.readthedocs.io/en/latest/) to get it done .
* This script has been deployed as clound function on google cloud run service AS [load-asset-price-yahoo](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_daily_price_from_yahoo.ipynb)(google cloud function) and create job on cloud scheduler to trig clound function on daily basis.

### [build_forecast_ts_lstm_model.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset%20-price-movement-LSTM-TimeSeries/build_forecast_ts_lstm_model.ipynb)
##### Youtube :  [2#1 Build Univariate Multi Step LSTM Models To Predict Stock Price](https://www.youtube.com/watch?v=O8p2cteVTSs&feature=youtu.be) | [2#2 Build Univariate Multi Step LSTM Models To Predict Stock Price](https://youtu.be/_bVOFtHC2yQ) |  [2#3 Build Univariate Multi Step LSTM Models To Predict Stock Price](https://www.youtube.com/watch?v=8idQEuBFLfw&feature=youtu.be)
* Loading the training data from Big1uery  and save it as   csv file.
* Exploring the data to identify trends and patterns of EMA movement.
* Splitting the data  into train/test dataset to prepare it for modeling.
* Scaling  data to Mix-Max Range 0-1.
* Creating feature  as 3 direction array , it is proper input format to feed into the LSTM network .
* Tuning model to find optimal hyper paramter to get best model.
* ReTraining with the best tuned model on the training data set.
* Evaluation with test dataset with selected regression metric to see how well model forecast  with metric MAE .
* Building final model with entire data .
* Storing model file and its scaler files into local path and GCS.


### [forecast_asset_movement.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/forecast_asset_movement.ipynb)
##### Youtube :[3 Make Stock Multi Step Prediction Using LSTM Model](https://www.youtube.com/watch?v=8DlACgKslSE)
* Load model configuration metadata by model-id from csv file referenced as external table on BigQuery.
* Load model file and scaler file for feature and prediction value normalization.
* Check whether price data as specifed data on FinAssetForecast.fin_data table have been made prediction on FinAssetForecast.fin_movement_forecast table .
* Get the last N sequence records of specific feature like EMA,MACD,SIGNAL as input feature from FinAssetForecast.fin_data table to make prediction future  movement as prediction output. 
* Make predction with proper input (3 dimesion numpy array  [sample rows, time steps, features])
* Create 3 dataframes and covert Json file, there are 2 dataframe containing feature and predictoin valu.e  Feature Dataframe are contained as collection in  Main Dataframe .
* Ingest JSON file into FinAssetForecast.fin_movement_forecast table.
* This script has been deployed as clound function on google cloud run service AS [forecast-asset-movement].(https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries/forecast-asset-movement) and create job on cloud scheduler to trig clound function on daily basis.

### [invoke_forecast_gcf](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/invoke_forecast_gcf.ipynb)
* To make prediction multiple items , run this script to call cloud function api by specifying desired period.
* To obtain authentication token as credential to call api correctly, you need to  install Google cloud-sdk and set defualt project first on enviroemnt variable(Window OS). [link](https://cloud.google.com/sdk/docs/install).


### [visualize_forecast_ts](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/visualize_forecast_ts.ipynb)
* Specify start-date and end-date to plot prediction result
* Get model configuration from FinAssetForecast.model_ts_metadata table by the model id.
* Get feature and  prediction value from FinAssetForecast.fin_movement_forecast and actual value from  FinAssetForecast.fin_movement_forecast.
* Plot prediction result consisted of feature value and prediction value consecutively by  comparison between prediction to actual price using line chart.
* Find mean absolute error(MAE) to measure gap between actual value and predicted value. 

###  [Prediction Result Analystics on PowerBI](https://app.powerbi.com/groups/me/reports/fa816185-f898-4b89-9d06-8864d39ec0eb/ReportSection?experience=power-bi)
* Show EMA features value series (blue dot) followed by EMA Prediction value (green dot).
* Retrive prediction result from view table in Bigquery.
* Transform  data in order to filter only EMA1 Feature.
* Create Visualization prection result(feature+prediction) compare to actual price with line chart on PowerBI.

### Folder to store Artifact and other files
* [model](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/model) :  Each sub folder stores model file and scaler object file, each is located on both local path and google cloud  storage.
* [model_ts_metadata.csv](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset%20-price-movement-LSTM-TimeSeries/model/model_ts_metadata.csv) : store model configuration metadata on google cloud storage but it allow you to query against external table on BigQuery.
* [train_data](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries/train_data) : store train/test csv file loaded from Bigquery.
* [train_model_collection](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries/train_model_collection) : All satisfactory models can be collected here.
* [tuning](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries/tuning) : use Keras Tuner to find optimal hyperparamer and store tuning result here.
* [csv_data](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries/csv_data) :To load data price exported from Amibrker to BQ, we will store this file here  .
* [data-schema-bq](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries/data-schema-bq) : all table schema on Bigquery.
* [command to deploy script to cloud function](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset%20-price-movement-LSTM-TimeSeries/forecast-asset-deploy-function.txt)  
