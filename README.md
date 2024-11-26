## Cryptocurrency return rate prediction project

### Dataset Introduction

This dataset was obtained from [Binance](https://www.binance.com/en-GB), one of the leading global cryptocurrency exchange. Binance offers comprehensive price data for both unified margin (UM) and cross margin (CM) in spot and futures trading, with data intervals ranging from seconds to daily timeframes. My research focuses specifically on futures trading data, analyzing one-minute klines (candlestick data) from February 1st, 2022 to March 31st, 2022 (all stored in BINAN folder). The `Binance.py` script demonstrates how to retrieve these datasets from [Binance History Data Repository](https://data.binance.vision/?prefix=data/futures/um/daily/klines/).

**Note**: Make sure to set your Google Drive download path to your desired target directory.

### Return Rate Prediction

The `RNN_prediction.ipynb` implements a Recurrent Neural Network (RNN) model for predicting price return rates in cryptocurrency trading. Instead of directly predicting absolute prices, we focus on the return rate, calculated as:

$r = \frac{P_1 - P_0}{P_0}$

Where:

$r$ represents the return rate

$P_1$ is the current price

$P_0$ is the previous price

This approach of predicting return rates rather than raw prices was chosen deliberately. When evaluating machine learning models in financial forecasting, using absolute prices as targets often leads to overestimated performance metrics. This can create a misleading impression of the model's actual predictive capabilities. Our methodology, inspired by research discussed in this [article](https://cloud.tencent.com/developer/article/2210127), aims to provide a more realistic assessment of the model's predictive power.

Furthermore, we evaluated the model's long-term forecasting capabilities. Rather than limiting our assessment to the traditional approach of using historical data points $T_{n-k}$ to $T_n$ to predict only the next timestep $T_{n+1}$, we extended our analysis to test the model's ability to forecast multiple steps ahead $T_{n+2}$, $T_{n+3}$, etc.. This multi-step prediction approach provides a more comprehensive evaluation of the model's performance in long-term time series forecasting.
