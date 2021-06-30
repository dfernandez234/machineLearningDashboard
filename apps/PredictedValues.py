import pandas as pd
import numpy as np
import os
from os.path import dirname
from apps import DataDictionaries


#states info
#https://dl.dropboxusercontent.com/s/082figxvvleq1zy/states.csv?dl=0
dsPath = os.getcwd() + '/codec/statesPred.csv'
statesData = pd.read_csv(dsPath, dtype={"code": str})
statesData['code'] = statesData['code'].apply(lambda x: '{0:0>2}'.format(x))

def statesDF():
    sd = statesData
    return sd

def read_result(indicator, state):
    if indicator == 1:
        dfPath = os.getcwd() + f"/codec/resultsIncCSV/{state}.csv"
        df = pd.read_csv(dfPath)
        df = df.drop(columns=['Unnamed: 0'])
        dates = pd.date_range(start='1/1/2010', periods=df.shape[0])
        datesCol = pd.DataFrame(dates)
        result = pd.concat([datesCol, df], axis=1)
        result.rename(columns={0:'day', 'trend':'toll'}, inplace=True)
        result.toll = result.toll.round(2)
        return result

    if indicator == 2:
        dfPath = os.getcwd() + f"/codec/resultsCSV/{state}.csv"
        df = pd.read_csv(dfPath)
        df = df.drop(columns=['Unnamed: 0'])
        dates = pd.date_range(start='1/1/2010', periods=df.shape[0])
        datesCol = pd.DataFrame(dates)
        result = pd.concat([datesCol, df], axis=1)
        result.rename(columns={0:'day', 'trend':'toll'}, inplace=True)
        result.toll = result.toll.round(2)
        return result


def get_daily(df):
    dff = df
    cut = dff.shape[0]
    originalData = dff[:cut - 12*15 + 1]
    predictedData = dff[cut - 12*15:] 
    return originalData, predictedData

def get_monthly(df):
    month = df.resample('M', on='day').sum()
    month.reset_index(inplace=True)
    cut = month.shape[0]
    originalData = month[:cut - 5]
    predictedData = month[cut - 6:month.shape[0]-1]
    return originalData, predictedData