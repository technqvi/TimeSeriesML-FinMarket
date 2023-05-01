# About
- These files are about how to build a time-series model to forecast eft-fund/stock/crypto(asset price) price movement, all of them do the same thing as [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb) but with different machine learning methods and input/output sequences.
- Mainly, We use several samples from  [flo7up-relataly-public-python-tutorials](https://github.com/flo7up/relataly-public-python-tutorials) to perform on my own experiement.

## Main Files

### [MultiVarToSingleOutLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/MultiVarToSingleOutLSTM.ipynb) 
- Using Multivariate Time Series and Recurrent Neural Networks(LSTM) to forecast price movement in advance.
- Use several input features such as PRice + MA1+ MACD+RSI to forecast one step into the future (Multivariate RNN forecasting models) like  you take data 60 days agoa  to predict in the next 1 day. 
- Reference Content&Code : [Stock Market Prediction using Multivariate Time Series and Recurrent Neural Networks in Python](https://www.relataly.com/stock-market-prediction-using-multivariate-time-series-in-python/1815/) | [007 Time Series Forecasting - Multivariate Time Series Models.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/007%20Time%20Series%20Forecasting%20-%20Multivariate%20Time%20Series%20Models.ipynb)


### [UnivariatePredictNextLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/UnivariatePredictNextLSTM.ipynb) 
- Creating a univariate model using a Keras neural network with LSTM  forecast the S&P500 ETF Fund by making single-step predictions for the stock market.
- Choose one input features such as Price , MA1, MACD and RSI to forecast one step into the future (Univariate RNN forecasting models)
- Reference Content&Code : [Stock Market Prediction using Univariate Recurrent Neural Networks (RNN) with Python](https://www.relataly.com/univariate-stock-market-forecasting-using-a-recurrent-neural-network/122/) | [003 Time Series Forecasting - Univariate Model using Recurrent Neural Networks.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/003%20Time%20Series%20Forecasting%20-%20Univariate%20Model%20using%20Recurrent%20Neural%20Networks.ipynb)


## Option Files
### [soubhik_univariae_lstm-finmarket.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/soubhik_univariae_lstm-finmarket.ipynb)
- LSTM  Univariate Time Series Forecasting to predict stock price movement.
- Reference Content: [Univariate Time Series Forecasting using RNN(LSTM)](https://medium.com/mlearning-ai/univariate-time-series-forecasting-using-rnn-lstm-32702bd5cf4)
### [soubhik_multi_lstm-finmarket.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/soubhik_multi_lstm-finmarket.ipynb)
- LSTM  Multivariate Time Series Forecasting to predict stock price movement.
- Reference Content: [Multivariate Time Series Forecasting using RNN(LSTM)](https://medium.com/mlearning-ai/multivariate-time-series-forecasting-using-rnn-lstm-8d840f3f9aa7)
### [Witchapong(Dev)-LSTM-ThaiStock.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/Witchapong(Dev)-LSTM-ThaiStock.ipynb)
- Reference Content: [Let's try simple stock price forecasting with Deep Learning — LSTM (Python)](https://medium.com/datawiz-th/%E0%B8%A1%E0%B8%B2%E0%B8%A5%E0%B8%AD%E0%B8%87-forecast-%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%AB%E0%B8%B8%E0%B9%89%E0%B8%99%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2%E0%B9%86-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-deep-learning-lstm-python-305c480db223)

### [torch_fin_market_Daniel](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/lstm-fin-asset/torch_fin_market_Daniel)
- Appy PyTorch framework to build Multivariate Time Series Forecasting model.
- Reference Content&Code : [Multivariate Time Series Forecasting with Deep Learning](https://towardsdatascience.com/multivariate-time-series-forecasting-with-deep-learning-3e7b3e2d2bcf) | [deep-forecasting](https://github.com/danielhkt/deep-forecasting)


### [RollingMultiStepUnivLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/RollingMultiStepUnivLSTM.ipynb)
- This approach will roll multi-step forecast to by taking previouse output as input  to predict the next one, it is not simialar to [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)
that the it will predict several points of a signal at once within a prediction window.
- Reference Content&Code: [Rolling Time Series Forecasting: Creating a Multi-Step Prediction for a Rising Sine Curve using Neural Networks in Python](https://www.relataly.com/multi-step-time-series-forecasting-a-step-by-step-guide/275/)  | [005 Time Series Forecasting - Multi-step Rolling Forecasting.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/005%20Time%20Series%20Forecasting%20-%20Multi-step%20Rolling%20Forecasting.ipynb)

### [ARIMA-Auto S&P500 with.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/ARIMA-Auto%20S%26P500%20with.ipynb) 
- Use ARIMA-AUTO to forecast S&P500 ETF price , USe one feature (univariate forecasting models) to predict one future values.
- Reference Content&Code : [Forecasting Beer Sales with ARIMA in Python](https://www.relataly.com/forecasting-beer-sales-with-arima-in-python/2884/) | [001 Time Series Forecasting - Forecasting US Beer Sales with (auto) ARIMA.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/001%20Time%20Series%20Forecasting%20-%20Forecasting%20US%20Beer%20Sales%20with%20(auto)%20ARIMA.ipynb)

