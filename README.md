# About
This project is about how to build time-series machine leaning to predict asset price(ETF-Fund,Stock, Crypto) and its technical indicators(Moving-Average,MACD,RSI). There are 2 parts such as Main-Section and Additional-Section , we focus on the former.
### Main Packages  on Python 3.9
- tensorflow >=2.11
- scikit-learn >= 1.2.2
- pandas >=1.5.3
- numpy >= 1.24.2
- matplotlib >=3.7.1

## Main-Section

### [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)
Use LSTM to build time-series forecasting to take price over the past 60 days to  predict price in the next 10 days.  It use [Stock Market Forecasting Neural Networks for Multi-Output Regression in Python](https://www.relataly.com/stock-price-prediction-multi-output-regression-using-neural-networks-in-python/5800/) as starting template to develop.
#### The steps performed include:
- Load Data from CSV file , we use [Amibroker](https://www.amibroker.com/) exploration to export price and create technical indicator feature such as exponential moving average ,MCD, RSI 
- Preprocess (MinMaxScaler) trand and test data and select features
- Convert data to window-sequence time-series format  for building LSTC like format of [sample, time steps, features]
- Build model and feed train data into designed model.
- Evaluate Model Performancel on the test data using Mean Absolute Error (MAE) and Root MEAN Square Error(RMSE)
- Plot Multiple Forecast
- Predict New Data
#### Source Code Reference: [006 Time Series Forecasting - Multi-Output Regression.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/006%20Time%20Series%20Forecasting%20-%20Multi-Output%20Regression.ipynb)


## Option-Section
