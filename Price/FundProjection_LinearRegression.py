import numpy as np
import pandas as pd
from sklearn.svm import SVR
import pandas_datareader.data as web
import datetime as dt
from datetime import timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from pymongo import MongoClient
import csv
import futureDates
import trainModel
pd.plotting.register_matplotlib_converters(explicit=True)

# ETF funds for testing the code. In live code this is a selection from UI
list_etf = ['VHT','VIS','VOX','VCR','VDC']
future_proj_days = 750 # Number of days in future for which values to be predicted. In live code this is user provided
dict_r2 = {} # Dictionary for storing r2 values
dict_fund_model = {} # Dictionary to store ETF funds and their corresponding model
start = dt.datetime(2005,1,1)
end = dt.datetime.today()
for etf in list_etf:
    model_etf = trainModel.TrainTestModel(etf)
    dict_r2[etf] = model_etf['r2']
    dict_fund_model[etf] = model_etf

dict_future_projection = {}
for etf_iterator in range(0,len(list_etf)):
    fund_lr_model = dict_fund_model[list_etf[etf_iterator]]
    r2_value = round(fund_lr_model['r2'],6)*100
    #coefficient = fund_lr_model['Coefficient'][0]
    #intercept = fund_lr_model['Intercept'][0]
    coefficient = fund_lr_model['Coefficient'][0]
    intercept = fund_lr_model['Intercept'][0]
    df_fund_model_dataset = pd.DataFrame(fund_lr_model['Test_Pred_data'])
    plt.plot(df_fund_model_dataset['Date'],df_fund_model_dataset['ActualPrice'])
    plt.plot(df_fund_model_dataset['Date'],df_fund_model_dataset['PredictedPrice'])
    plt.title(f'Performance Trend for {list_etf[etf_iterator]} with confidence level of {r2_value}% \n')
    #plt.show()
    image_name = 'Projection_' + list_etf[etf_iterator] + '.png'
    plt.savefig(image_name)
    # Predicting future values
    df_future_projection = futureDates.createFutureDates(future_proj_days)
    df_future_projection['FutureValue'] = ((df_future_projection['DateFloat']).values.reshape(-1,1) * coefficient) + intercept
    dict_future_projection[list_etf[etf_iterator]] = df_future_projection
    #df_future_projection['FutureValue'] = ((df_future_projection['DateFloat']) * coefficient) + intercept
    file_name = 'FutureProjections_' + list_etf[etf_iterator] + '.csv'
    #image_future_projection = 'FutureProjections_' + list_etf[etf_iterator] + '.csv'
    df_future_projection.to_csv(file_name)
    # This part of code is to plot future value graph. This is irrelevant since with LR model growth/fall will always
    # be in a straight line. To test, you can un-comment these code-lines.
    #plt.plot(df_future_projection['Date'], df_future_projection['FutureValue'])
    #plt.title(f'Future growth pattern for {list_etf[etf_iterator]} with confidence level of {r2_value}% \n')
    #plt.show()