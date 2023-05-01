# About
- These files are about how to build a time-series model to forecast eft-fund/stock/crypto(asset price) price movement, all of them do the same thing as [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb) but with different machine learning methods and input/output sequences.
- Mainly, We use several samples from  [flo7up-relataly-public-python-tutorials](https://github.com/flo7up/relataly-public-python-tutorials) to perform on my own experiement.

## Main Files

### [MultiVarToSingleOutLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/MultiVarToSingleOutLSTM.ipynb) 
- Using Multivariate Time Series and Recurrent Neural Networks(LSTM) to forecast price movement in advance.
- Use several input features such as PRice + MA1+ MACD+RSI to forecast price one day ahead (Multivariate RNN forecasting models)
- Reference Content&Code : [Stock Market Prediction using Multivariate Time Series and Recurrent Neural Networks in Python](https://www.relataly.com/stock-market-prediction-using-multivariate-time-series-in-python/1815/) | [007 Time Series Forecasting - Multivariate Time Series Models.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/007%20Time%20Series%20Forecasting%20-%20Multivariate%20Time%20Series%20Models.ipynb)


### [UnivariatePredictNextLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/UnivariatePredictNextLSTM.ipynb) 
- Creating a univariate model using a Keras neural network with LSTM  forecast the S&P500 ETF Fund by making single-step predictions for the stock market.
- Choose one input features such as Price , MA1, MACD and RSI to forecast price one day ahead (Univariate RNN forecasting models)
- Reference Content&Code : [Stock Market Prediction using Univariate Recurrent Neural Networks (RNN) with Python](https://www.relataly.com/univariate-stock-market-forecasting-using-a-recurrent-neural-network/122/) | [003 Time Series Forecasting - Univariate Model using Recurrent Neural Networks.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/003%20Time%20Series%20Forecasting%20-%20Univariate%20Model%20using%20Recurrent%20Neural%20Networks.ipynb)


## Option Files

### [RollingMultiStepUnivLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/RollingMultiStepUnivLSTM.ipynb)





### [ARIMA-Auto S&P500 with.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/ARIMA-Auto%20S%26P500%20with.ipynb) 
- Use ARIMA-AUTO to forecast S&P500 ETF price , USe one feature (univariate forecasting models) to predict one future values.
- Reference Content&Code : [Forecasting Beer Sales with ARIMA in Python](https://www.relataly.com/forecasting-beer-sales-with-arima-in-python/2884/) | [001 Time Series Forecasting - Forecasting US Beer Sales with (auto) ARIMA.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/001%20Time%20Series%20Forecasting%20-%20Forecasting%20US%20Beer%20Sales%20with%20(auto)%20ARIMA.ipynb)

