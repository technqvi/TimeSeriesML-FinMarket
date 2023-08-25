# About
This project is about how to build time-series model using Long short-term memory (LSTM) network to predict asset price(ETF-Fund,Stock, Crypto) and its technical indicators(Moving-Average,MACD,RSI). Mainly there are 3 parts such as Main Project  ,Main-Section and Additional-Section.

## Main Project : [forecast-asset -price-movement-LSTM-TimeSeries](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset%20-price-movement-LSTM-TimeSeries) .
### Main Tutorial on Youtube : [Building LSTM Time-Series Models to Predict Future Stock Price Movement](https://www.youtube.com/playlist?list=PLIxgtZc_tZWPCX4dAFJFhDPPGxEungxc8)

<img width="839" alt="image" src="https://github.com/technqvi/TimeSeriesML-FinMarket/assets/38780060/8306119d-1399-4aa5-8d3d-0c968161f5a3">



## Main-Section 

### [Build LSTM Time-Series](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)
#### Overview
- Run this file to build model [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)
- This is one of the core files on this repo,  we apply the LSTM model to build time-series forecasting to take prices over the past 60 days to predict prices in the next 10 days.
- The first cell of this file include steps to build model from loading data to making prediction to unseen data.
- It allows you to select what you want to predict as single columns as output but predict multiple outcomes in advance, for instance, you take MA10 , MACD, and RSI  60 days ago to predict Price in the next 10 day. 
- In addition to price as single input features(univariate time ),   you can choose others like MACD, SIGNAL,EMA,RSI as well as a mixture of these features as multiple features(multivariate) to feed into the model to predict. 
#### References
- Document: [1-Stock Market Forecasting Neural Networks for Multi-Output Regression in Python](https://www.relataly.com/stock-price-prediction-multi-output-regression-using-neural-networks-in-python/5800/) | [2-Stock Market Prediction using Univariate Recurrent Neural Networks (RNN) with Python](https://www.relataly.com/univariate-stock-market-forecasting-using-a-recurrent-neural-network/122/) | [3-Multivariate Time Series and Recurrent Neural Networks in Python](https://www.relataly.com/stock-market-prediction-using-multivariate-time-series-in-python/1815/)  | [Measuring Regression Errors](https://www.relataly.com/regression-error-metrics-python/923/)
- SourceCode: [006 Time Series Forecasting - Multi-Output Regression.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/01%20Time%20Series%20Forecasting%20%26%20Regression/006%20Multi-Output%20Regression.ipynb)


### [Tune LSTM Time-Series using Keras-Tuner](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/lstm-tune-dev)
#### [Tuned-MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tuned-MultiVarToManyOutputLSTM.ipynb)
- [Tuned-MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tuned-MultiVarToManyOutputLSTM.ipynb) :  To find optimal hypperparamter to get the best model, we apply KerasTuner to perform this thing. we tuned 2 stuff ,   Input-Unit on hidden layer and Dropout-Rate . we added tuning code part(Training the TUNED Model) into this file. The remaining  is  the same as  [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb) 
- [Tune_jsbl-GenTS-multiI-InToOut.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tune_jsbl-GenTS-multiI-InToOut.ipynb): Build time series model to forecast multiple technical indicators like EMA,MACD,Signal,RSI at the same time, each of them will take its own data in the past to predict future data simultaneously and separately.
- [all-kind-of-lstm-network](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/all-kind-of-lstm-network.txt) : there are variouse LSTM Network design as stating point for tuning hypter-paramters.

#### [Tune_jsbl-GenTS-multiI-InToOut.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tune_jsbl-GenTS-multiI-InToOut.ipynb)
- Use Keras TimeseriesGenerator for preparing time series  
- It is multiple parallel series at the same time step in each series concurrently.
- For example, take Price,MACD, RSI in the past 20 days to predict each of them in the next 5 days simultaneously.  each of them forecasts future value on its own separately. 
- Reference content : [How to Use the TimeseriesGenerator for Time Series Forecasting in Keras](https://machinelearningmastery.com/how-to-use-the-timeseriesgenerator-for-time-series-forecasting-in-keras/)
 
### [Practice building TS-Model by Examples](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/lstm-fin-asset)
click  link to see detail.

## Option-Section

#### [lstm-jason-brownlee](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/lstm-jason-brownlee)
There are a lot of files that we do some research regarding how to build LSTM Time-Series   of  [machinelearningmastery.com powered by Jason Brownlee](https://machinelearningmastery.com/)
- [How to Develop LSTM Models for Time Series Forecasting](https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/)
- [Time Series Forecasting as Supervised Learning](https://machinelearningmastery.com/time-series-forecasting-supervised-learning/)
- [How to Use the TimeseriesGenerator for Time Series Forecasting in Keras](https://machinelearningmastery.com/how-to-use-the-timeseriesgenerator-for-time-series-forecasting-in-keras/)
- [Multivariate Time Series Forecasting with LSTMs in Keras](https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/)
- [How to Develop LSTM Models for Time Series Forecasting](https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/ )


#### [additional_dev](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/additional_dev)

#### Keras Tuner Refernces
- [Getting Started with KerasTuner](https://keras.io/guides/keras_tuner/getting_started/)
- [Introduction to the Keras Tuner](https://www.tensorflow.org/tutorials/keras/keras_tuner)
- [BayesianOptimization Tuner](https://keras.io/api/keras_tuner/tuners/bayesian/)

### Main Packages  on Python 3.9
- tensorflow >=2.11
- scikit-learn >= 1.2.2
- pandas >=1.5.3 and numpy >= 1.24.2
- ta =0.10.2