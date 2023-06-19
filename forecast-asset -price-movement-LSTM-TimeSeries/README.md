# About
This is experimental project to guid you how to predict stock price movement pattern pattern with End to End Solution .
Load Data => Build Model ==> Forecast Model ==> Deploy Model ==> Visualize Forecasting Result

## [Forecast-Asset from Trained Model](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset)
#### [load_daily_price_from_yahoo.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_daily_price_from_yahoo.ipynb)
* There are 2 options to load price data to GoogleBiquery.
* Option#1 Export data price from Amibroker as csv file and load it to bigquery.
* Option#2 Pull data price from [finance.yahoo.com](https://finance.yahoo.com/) by using [yfinance](https://github.com/ranaroussi/yfinance) as dataframe and load it to bigquery 
* To build any technical analysis indicator as feature to get prepred for building Time-Series Machine Learning, we can appy [Technical Analysis Library in Python](https://technical-analysis-library-in-python.readthedocs.io/en/latest/) to do it 


* [load-asset-price-yahoo](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_daily_price_from_yahoo.ipynb)(google cloud function), we will deploy [load_asset_price_yahoo.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_asset_price_yahoo.ipynb) as clound function on google cloud run service.
#### [forecast_asset_movement.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/forecast_asset_movement.ipynb)
* [forecast-asset-movement](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/forecast-asset-movement)(google cloud function)
#### [visualize_forecast_ts](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/visualize_forecast_ts.ipynb)
#### [invoke_forecast_gcf](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/invoke_forecast_gcf.ipynb)
#### [model](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/model)



### [data](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/data)
This directory contains several csv file to be used as input data to run these script files such as  [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)

### [models](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/models)
This directory contains model file ,scaler files and  experimental result.