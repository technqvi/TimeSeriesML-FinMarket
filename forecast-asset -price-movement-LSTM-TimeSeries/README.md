# About
This is experimental project to guid you how to predict stock price movement pattern pattern with End to End Solution .
Load Data => Build Model ==> Forecast Model ==> Deploy Model ==> Visualize Forecasting Result

## [Forecast Asset Future Price Movement By LSTM-TimeSeries](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset)
### [load_daily_price_from_yahoo.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_daily_price_from_yahoo.ipynb)
##### Youtube : [ Load Stock Price From Yahoo To BigQuery For Building LSTM Model](https://www.youtube.com/watch?v=jaPpyopNFPA&feature=youtu.be)
* There are 2 options to load price data to GoogleBiquery.
* Option#1 Export data price from Amibroker as csv file and load it to bigquery.
* Option#2 Pull data price from [finance.yahoo.com](https://finance.yahoo.com/) by using [yfinance](https://github.com/ranaroussi/yfinance) as dataframe and load it to bigquery 
* To build any technical analysis indicator as features to get prepred for building Time-Series Machine Learning, we can appy [Technical Analysis Library in Python](https://technical-analysis-library-in-python.readthedocs.io/en/latest/) to get it done 
* This script has been deployed as clound function on google cloud run service.  [load-asset-price-yahoo](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_daily_price_from_yahoo.ipynb)(google cloud function)
### [build_forecast_ts_lstm_model.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset%20-price-movement-LSTM-TimeSeries/build_forecast_ts_lstm_model.ipynb)
##### Youtube :  [2#1 Build Univariate Multi Step LSTM Models To Predict Stock Price](https://www.youtube.com/watch?v=uElXlUZQ1_M&feature=youtu.be) 
* Loading the training data from Big1uery  and save it as   csv file
* Exploring the data to identify trends and patterns of EMA movement
* Splitting the data  into train/test dataset to prepare it for modeling
* Scaling  data to Mix-Max Range 0-1
* Creating feature  as 3 direction array , it is proper input format to feed into the LSTM network 
* Tuning model to find optimal hyper paramter to get best model
* ReTraining with the best tuned model on the training data set
* Evaluation with test dataset with selected regression metric to see how well model forecast  with metric MAE 
* Building final model with entire data 
* Storing model file and its scaler file into local path and GCS


#### [forecast_asset_movement.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/forecast_asset_movement.ipynb)
* [forecast-asset-movement](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/forecast-asset-movement)(google cloud function)
#### [visualize_forecast_ts](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/visualize_forecast_ts.ipynb)
#### [invoke_forecast_gcf](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/invoke_forecast_gcf.ipynb)
#### [model](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/model)



### [data](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/data)
This directory contains several csv file to be used as input data to run these script files such as  [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)

### [models](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/models)
This directory contains model file ,scaler files and  experimental result.