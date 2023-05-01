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
- This is one of the core files on this repo,  we apply the LSTM model to build time-series forecasting to take prices over the past 60 days to predict prices in the next 10 days.
- This allows you to select what you want to predict as single columns as output but predict multiple outcomes in advance, for instance, you take MA10 , MACD, and RSI  60 days ago to predict Price in the next 10 day. 
- In addition to price as input features,   you can choose others like MACD, SIGNAL,EMA,RSI as well as a mixture of these features as multiple features to feed into the model to predict  
- Document Reference : [Stock Market Forecasting Neural Networks for Multi-Output Regression in Python](https://www.relataly.com/stock-price-prediction-multi-output-regression-using-neural-networks-in-python/5800/).
- Source Code Reference: [006 Time Series Forecasting - Multi-Output Regression.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/006%20Time%20Series%20Forecasting%20-%20Multi-Output%20Regression.ipynb)

### 


## Option-Section
