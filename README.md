# About
This project is about how to build time-series machine leaning to predict asset price(ETF-Fund,Stock, Crypto) and its technical indicators(Moving-Average,MACD,RSI). There are 2 parts such as Main-Section and Additional-Section , we focus on the former.
### Main Packages  on Python 3.9
- tensorflow >=2.11
- scikit-learn >= 1.2.2
- pandas >=1.5.3 and numpy >= 1.24.2

## Main-Section

### [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)
#### Overview
- This is one of the core files on this repo,  we apply the LSTM model to build time-series forecasting to take prices over the past 60 days to predict prices in the next 10 days.
- The first cell of this file include steps to build model from loading data to making prediction to unseen data.
- It allows you to select what you want to predict as single columns as output but predict multiple outcomes in advance, for instance, you take MA10 , MACD, and RSI  60 days ago to predict Price in the next 10 day. 
- In addition to price as single input features(univariate time ),   you can choose others like MACD, SIGNAL,EMA,RSI as well as a mixture of these features as multiple features(multivariate) to feed into the model to predict. 
#### References
- Document: [Stock Market Forecasting Neural Networks for Multi-Output Regression in Python](https://www.relataly.com/stock-price-prediction-multi-output-regression-using-neural-networks-in-python/5800/)
- SourceCode: [006 Time Series Forecasting - Multi-Output Regression.ipynb](https://github.com/flo7up/relataly-public-python-tutorials/blob/master/006%20Time%20Series%20Forecasting%20-%20Multi-Output%20Regression.ipynb)

### [forecast-asset](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset)
#### [load_price_asset_yahoo.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/load_asset_price_yahoo.ipynb)
* []load-asset-price-yahoo (google cloud function)] (https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/load-asset-price-yahoo)
* [forecast-asset-movement](google cloud function)](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/forecast-asset-movement)
#### [forecast_asset_movement.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/forecast_asset_movement.ipynb)
* [forecast-asset-movement](google cloud function)](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/forecast-asset-movement)
#### [visualize_forecast_ts](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/visualize_forecast_ts.ipynb)
#### [invoke_forecast_gcf](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/forecast-asset/invoke_forecast_gcf.ipynb)
#### [model](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/forecast-asset/model)



### [lstm-tune-dev](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/lstm-tune-dev)
#### [Tuned-MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tuned-MultiVarToManyOutputLSTM.ipynb)

- [Tuned-MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tuned-MultiVarToManyOutputLSTM.ipynb) :  To find optimal hypperparamter to get the best model, we apply KerasTuner to perform this thing. we tuned 2 stuff ,   Input-Unit on hidden layer and Dropout-Rate . we added tuning code part(Training the TUNED Model) into this file. The remaining  is  the same as  [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb) 
- [Tune_jsbl-GenTS-multiI-InToOut.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tune_jsbl-GenTS-multiI-InToOut.ipynb): Build time series model to forecast multiple technical indicators like EMA,MACD,Signal,RSI at the same time, each of them will take its own data in the past to predict future data simultaneously and separately.
- [all-kind-of-lstm-network](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/all-kind-of-lstm-network.txt) : there are variouse LSTM Network design as stating point for tuning hypter-paramters.

#### [Tune_jsbl-GenTS-multiI-InToOut.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/lstm-tune-dev/Tune_jsbl-GenTS-multiI-InToOut.ipynb)
- Use Keras TimeseriesGenerator for preparing time series  
- It is multiple parallel series at the same time step in each series concurrently.
- For example, take Price,MACD, RSI in the past 20 days to predict each of them in the next 5 days simultaneously.  each of them forecasts future value on its own separately. 
- Reference content : [How to Use the TimeseriesGenerator for Time Series Forecasting in Keras](https://machinelearningmastery.com/how-to-use-the-timeseriesgenerator-for-time-series-forecasting-in-keras/)
 


### [lstm-fin-asset](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/lstm-fin-asset)
click  link to see detail.

### [data](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/data)
This directory contains several csv file to be used as input data to run these script files such as  [MultiVarToManyOutputLSTM.ipynb](https://github.com/technqvi/TimeSeriesML-FinMarket/blob/main/MultiVarToManyOutputLSTM.ipynb)

### [models](https://github.com/technqvi/TimeSeriesML-FinMarket/tree/main/models)
This directory contains model file ,scaler files and  experimental result.



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