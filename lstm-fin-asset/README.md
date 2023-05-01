# About
-These files are about how to build a time-series model to forecast eft-fund/stock/crypto(asset price) price movement, all of them do the same thing as [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb) but with different machine learning methods and input/output sequences.
- Mainly, We apply several samples from this [flo7up-relataly-public-python-tutorials](https://github.com/flo7up/relataly-public-python-tutorials) to perform on the experiement.
### [ARIMA-Auto S&P500 with.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/ARIMA-Auto%20S%26P500%20with.ipynb) 
- Use ARIMA-AUTO to forecast S&P500 ETF price , USe one feature (univariate forecasting models) to predict one future values.
- Reference Content&Code : [Forecasting Beer Sales with ARIMA in Python](https://www.relataly.com/forecasting-beer-sales-with-arima-in-python/2884/) | [001 Time Series Forecasting - Forecasting US Beer Sales with (auto) ARIMA.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/001%20Time%20Series%20Forecasting%20-%20Forecasting%20US%20Beer%20Sales%20with%20(auto)%20ARIMA.ipynb)

### [MultiVarToSingleOutLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-fin-asset/MultiVarToSingleOutLSTM.ipynb) 
- Using Multivariate Time Series and Recurrent Neural Networks(LSTM) to forecast price movement in advance.
- Use several input features such as PRice + MA1_MACD+RSI to forecast price one day ahead (Multivariate RNN forecasting models)
- Reference Content&Code : [Stock Market Prediction using Multivariate Time Series and Recurrent Neural Networks in Python](https://www.relataly.com/stock-market-prediction-using-multivariate-time-series-in-python/1815/) | [007 Time Series Forecasting - Multivariate Time Series Models.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/007%20Time%20Series%20Forecasting%20-%20Multivariate%20Time%20Series%20Models.ipynb)

