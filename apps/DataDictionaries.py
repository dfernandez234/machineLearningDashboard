import pandas as pd
import numpy as np
import os
from os.path import dirname

def read_year_csv(year, indicator):
    if indicator == 1:
        dfPath = os.getcwd() + f"/codec/incidence/Inc_{str(year)}.csv"
        df = pd.read_csv(dfPath)
        df['ent_regis'] = df['ent_regis'].apply(lambda x: '{0:0>2}'.format(x))
        index_names = df[((df['ent_regis'] > '32'))].index
        df.drop(index_names, inplace = True) 
        df = df.drop(columns=['Unnamed: 0'])
        return df
    if indicator == 2:
        dfPath = os.getcwd() + f"/codec/{str(year)}.csv"
        df = pd.read_csv(dfPath)
        df['ent_regis'] = df['ent_regis'].apply(lambda x: '{0:0>2}'.format(x))
        df['ent_resid'] = df['ent_resid'].apply(lambda x: '{0:0>2}'.format(x))
        df['ent_ocurr'] = df['ent_ocurr'].apply(lambda x: '{0:0>2}'.format(x))
        df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1','Unnamed: 0.1.1'])
        return df

#states info
#https://dl.dropboxusercontent.com/s/082figxvvleq1zy/states.csv?dl=0
dsPath = os.getcwd() + '/codec/states.csv'
statesData = pd.read_csv(dsPath, dtype={"code": str})
statesData['code'] = statesData['code'].apply(lambda x: '{0:0>2}'.format(x))

#cancer info
#https://dl.dropboxusercontent.com/s/fgx9mz0o2x6z1fj/types.csv?dl=0
dcPath = os.getcwd() + '/codec/types.csv'
cancData = pd.read_csv(dcPath)

#cancer dictionary
cancDict = cancData
cancDict.set_index('ICD', inplace=True)
cancDict = cancDict.to_dict()['organ']

#states dictionary
stateDict = statesData
stateDict = stateDict.groupby('code')[['state', 'lat', 'lon']].apply(lambda g: g.values.tolist()).to_dict()


#population dictionary
#https://dl.dropboxusercontent.com/s/ihun7h2mkhwgell/population.csv?dl=0
dpPath = os.getcwd() + '/codec/population.csv'
popInfo = pd.read_csv(dpPath)
popInfo.set_index('year', inplace=True)
popDict = popInfo.to_dict()['population']

#getters
def mainDF(year, indicator):
    dff = read_year_csv(year, indicator)
    return dff

def statesDF():
    sd = statesData
    return sd

def cancerDF():
    cd = cancData
    cd = cd.reset_index()
    return cd

def getCancDict():
    return cancDict

#utility functions for creating dictionaries from codec
def getStateKey(code):
    return stateDict.get(code)

def getCancerKey(icd):
    if isinstance(icd, list):
        if not icd:
            return ""
        ret_list = []
        for item in icd:
            ret_list.append(str(cancDict.get(item))+" ")
        return ret_list
    else:
        return cancDict.get(icd)


def getSex(gender_chosen):
    if gender_chosen == 1:
        gender_out = "Males"
    elif gender_chosen == 2:
        gender_out = "Females"
    else:
        gender_out = "Both"
    return gender_out

def getIndic(indicator):
    if indicator == 1:
        return 'indicence'
    if indicator == 2:
        return 'mortality'

def getPopulationNational(year):
    return popDict.get(year)

def solveQuery(year, gender, icd, age_range, indicator):
    dff = read_year_csv(year, indicator)
    if (isinstance(icd, list) and not icd) or (isinstance(icd, str) and not icd):
        dff = dff.loc[(dff['sexo'] == 2) & (dff['anio_ocur'] == 2012)]
        dff = dff.groupby(["ent_regis"])["ICD"].apply(lambda x: (x=="C16").sum()).reset_index(name='counts')
        dff.rename(columns={'ent_regis':'unique_values'}, inplace=True)
        dff['counts'] = 0
        return dff
    #initial query
    if(icd == 'c999' or 'C999' in icd):
        dff = dff.loc[(dff['sexo'] == gender) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
        dff =  dff['ent_regis'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        dff = dff.sort_values(by=['unique_values'])
        dff['unique_values'] = dff['unique_values'].apply(lambda x: '{0:0>2}'.format(x))
        dff.reset_index(drop=True, inplace=True)
        return dff
    else:
        cols = icd
        if(len(cols) == 1):
            dff = dff.loc[(dff['sexo'] == gender) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dff = dff.groupby(["ent_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name='counts')
            dff.rename(columns={'ent_regis':'unique_values'}, inplace=True)
            return dff
        else:
            #condition
            dff = dff.loc[(dff['sexo'] == gender) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dfcond = dff
            dff = dff.groupby(["ent_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name=cols[0])
            for i in range (1, len(cols)):
                currdf = dfcond.groupby(["ent_regis"])["ICD"].apply(lambda x: (x==cols[i]).sum()).reset_index(name='count')
                name = cols[i]
                new_col = currdf["count"]
                dff.insert(i+1, column=name, value=new_col)
            dff['counts'] = dff[cols].apply(lambda row: sum(row.values), axis=1)
            dff.drop(columns=cols,inplace=True)
            dff.rename(columns={'ent_regis':'unique_values'}, inplace=True)
            return dff




def solveQueryBothSexes(year, icd, age_range, indicator):
    dff = read_year_csv(year, indicator)
    if (isinstance(icd, list) and not icd) or (isinstance(icd, str) and not icd):
        dff = dff.loc[(dff['sexo'] == 2) & (dff['edad'] == 50) & (dff['anio_ocur'] == 2012)]
        dff = dff.groupby(["ent_regis"])["ICD"].apply(lambda x: (x=="C16").sum()).reset_index(name='counts')
        dff.rename(columns={'ent_regis':'unique_values'}, inplace=True)
        return dff
    #initial query
    if(icd == 'c999' or 'C999' in icd):
        dff = dff.loc[(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
        dff =  dff['ent_regis'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        dff = dff.sort_values(by=['unique_values'])
        dff['unique_values'] = dff['unique_values'].apply(lambda x: '{0:0>2}'.format(x))
        dff.reset_index(drop=True, inplace=True)
        return dff
    else:
        cols = icd
        if(len(cols) == 1):
            dff = dff.loc[(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dff = dff.groupby(["ent_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name='counts')
            dff.rename(columns={'ent_regis':'unique_values'}, inplace=True)
            return dff
        else:
            #condition
            dff = dff.loc[(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dfcond = dff
            dff = dff.groupby(["ent_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name=cols[0])
            for i in range (1, len(cols)):
                currdf = dfcond.groupby(["ent_regis"])["ICD"].apply(lambda x: (x==cols[i]).sum()).reset_index(name='count')
                name = cols[i]
                new_col = currdf["count"]
                dff.insert(i+1, column=name, value=new_col)
            dff['counts'] = dff[cols].apply(lambda row: sum(row.values), axis=1)
            dff.drop(columns=cols,inplace=True)
            dff.rename(columns={'ent_regis':'unique_values'}, inplace=True)
            return dff    

def generate_report(year, age_range, indicator):
    dff = read_year_csv(year, indicator)
    dff = dff.loc[(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
    curr_count = dff['ICD'].value_counts().rename_axis('unique_values').reset_index(name='counts')
    col_one_list = curr_count['unique_values'].tolist()
    output = list()
    for i in col_one_list:
        add_row = dff.loc[(dff['ICD'] == i) & (dff['sexo'] == 1)]
        add_row = add_row['ICD'].value_counts()
        if len(add_row.values) > 0:
            output.append(add_row.values[0])
        else:
            output.append(0)
    curr_count['male'] = output
    cols = ['counts', 'male']
    curr_count['female'] = curr_count['counts'] - curr_count['male']

    curr_count['Organ'] = curr_count['unique_values'].map(cancDict)

    curr_count['Rate'] = round((curr_count['counts']/popDict.get(year))*100000, 3)
    cols = dff.columns.tolist()
    cols = ['unique_values', 'Organ', 'male', 'female', 'counts', 'Rate']
    curr_count = curr_count[cols]
    curr_count.columns = ['ICD', 'Organ', 'Male Cases', 'Female Cases', 'Total Cases', 'Death Rate per 100,000']
    return curr_count

def generate_report_suburst(year, age_range, indicator):
    dff2 = read_year_csv(year, indicator)
    gender = [1,2]
    result = list()
    for i in gender:
        dff = dff2
        dff = dff.loc[(dff['sexo'] == i)&(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
        curr_count = dff['ICD'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        if i==1:
            curr_count['Gender'] = 'Female'
        else:
            curr_count['Gender'] = 'Male'
        result.append(curr_count[:9])
    ret = pd.concat(result)
    ret.reset_index(inplace=True)
    ret['Organ'] = curr_count['unique_values'].map(cancDict)
    del ret['index']
    return ret

def generate_time_series(year, age_range, indicator):
    dff = read_year_csv(year, indicator)
    dff = dff.loc[(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
    curr_count = dff['ICD'].value_counts().rename_axis('unique_values').reset_index(name='counts')
    col_one_list = list(cancDict.keys())
    month_count = dff['month_year_ocurr'].value_counts().rename_axis('Month').reset_index(name='C99')

    for i in range (1, len(col_one_list)):
        currdf = dff.groupby(["month_year_ocurr"])["ICD"].apply(lambda x: (x==col_one_list[i]).sum()).reset_index(name='count')
        name = col_one_list[i]
        new_col = currdf["count"]
        month_count.insert(i+1, column=name, value=new_col)

    month_count = month_count.sort_values(by=['Month'])
    return month_count