import pandas as pd
import numpy as np
import os
from os.path import dirname
from apps import DataDictionaries


#state filling
#https://dl.dropboxusercontent.com/s/j153iiqa8u1pexs/Municipalities.csv?dl=0
dmPath = os.getcwd() + '/codec/Municipalities.csv'
municipalities = pd.read_csv(dmPath)
municipalities = municipalities.drop(columns=['Unnamed: 0'])
municipalities['Clave_Entidad'] = municipalities['Clave_Entidad'].apply(lambda x: '{0:0>2}'.format(x))

municipalitiesDict = municipalities
municipalitiesDict = municipalitiesDict.groupby('Clave_Mun')[['Clave_Entidad', 'Nombre', 'Nombre_Municipio']].apply(lambda g: g.values.tolist()).to_dict()

def getMunKey(mun):
    return municipalitiesDict.get(mun)

#fill missing municipalities
def fillMissingMuns(dataFrame, state):
    stateFill = municipalities
    stateFill['initial_count'] = 0
    state = stateFill.loc[(stateFill['Clave_Entidad'] == state)]
    state.set_index('Clave_Mun', inplace=True)
    state = state.to_dict()['initial_count']
    state2 = dataFrame
    state2.set_index('unique_values', inplace=True)
    state2 = state2.to_dict()['counts']
    state.update(state2)
    stateUpdated = pd.DataFrame(list(state.items()), columns=['unique_values', 'counts'])
    return stateUpdated

def solveQueryState(year, gender, icd, age_range, state, indicator):
    dff = DataDictionaries.mainDF(year, indicator)
    if (isinstance(icd, list) and len(icd)<=0) or (isinstance(icd, str) and not icd):
        dff = dff.loc[(dff['ent_regis'] == state) & (dff['sexo'] == 2) & (dff['edad'] == 50)]
        dff = dff.groupby(["mun_regis"])["ICD"].apply(lambda x: (x=="C16").sum()).reset_index(name='counts')
        dff.rename(columns={'mun_regis':'unique_values'}, inplace=True)
        dff = fillMissingMuns(dff, state)
        return dff
    #initial query
    if(icd == 'c999' or 'C999' in icd):
        dff = dff.loc[(dff['ent_regis'] == state) & (dff['sexo'] == gender) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
        dff =  dff['mun_regis'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        dff = dff.sort_values(by=['unique_values'])
        dff['unique_values'] = dff['unique_values'].apply(lambda x: '{0:0>2}'.format(x))
        dff.reset_index(drop=True, inplace=True)
        dff = fillMissingMuns(dff, state)
        return dff
    else:
        cols = icd
        if(len(cols) == 1):
            dff = dff.loc[(dff['ent_regis'] == state) & (dff['sexo'] == gender) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dff = dff.groupby(["mun_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name='counts')
            dff.rename(columns={'mun_regis':'unique_values'}, inplace=True)
            dff = fillMissingMuns(dff, state)
            return dff
        else:
            #condition
            dff = dff.loc[(dff['ent_regis'] == state) & (dff['sexo'] == gender) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dfcond = dff
            dff = dff.groupby(["mun_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name=cols[0])
            for i in range (1, len(cols)):
                currdf = dfcond.groupby(["mun_regis"])["ICD"].apply(lambda x: (x==cols[i]).sum()).reset_index(name='count')
                name = cols[i]
                new_col = currdf["count"]
                dff.insert(i+1, column=name, value=new_col)
            dff['counts'] = dff[cols].apply(lambda row: sum(row.values), axis=1)
            dff.drop(columns=cols,inplace=True)
            dff.rename(columns={'mun_regis':'unique_values'}, inplace=True)
            dff = fillMissingMuns(dff, state)
            return dff


def solveQueryBothSexesState(year, icd, age_range, state, indicator):
    dff = DataDictionaries.mainDF(year, indicator)
    if (isinstance(icd, list) and len(icd)<=0) or (isinstance(icd, str) and not icd):
        dff = dff.loc[(dff['ent_regis'] == state) & (dff['sexo'] == 2) & (dff['edad'] == 50)]
        dff = dff.groupby(["mun_regis"])["ICD"].apply(lambda x: (x=="C16").sum()).reset_index(name='counts')
        dff.rename(columns={'mun_regis':'unique_values'}, inplace=True)
        dff = fillMissingMuns(dff, state)
        return dff
    #initial query
    if(icd == 'c999' or 'C999' in icd):
        dff = dff.loc[(dff['ent_regis'] == state) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
        dff =  dff['mun_regis'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        dff = dff.sort_values(by=['unique_values'])
        dff['unique_values'] = dff['unique_values'].apply(lambda x: '{0:0>2}'.format(x))
        dff.reset_index(drop=True, inplace=True)
        dff = fillMissingMuns(dff, state)
        return dff
    else:
        cols = icd
        if(len(cols) == 1):
            dff = dff.loc[(dff['ent_regis'] == state) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dff = dff.groupby(["mun_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name='counts')
            dff.rename(columns={'mun_regis':'unique_values'}, inplace=True)
            dff = fillMissingMuns(dff, state)
            return dff
        else:
            #condition
            dff = dff.loc[(dff['ent_regis'] == state) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
            dfcond = dff
            dff = dff.groupby(["mun_regis"])["ICD"].apply(lambda x: (x==cols[0]).sum()).reset_index(name=cols[0])
            for i in range (1, len(cols)):
                currdf = dfcond.groupby(["mun_regis"])["ICD"].apply(lambda x: (x==cols[i]).sum()).reset_index(name='count')
                name = cols[i]
                new_col = currdf["count"]
                dff.insert(i+1, column=name, value=new_col)
            dff['counts'] = dff[cols].apply(lambda row: sum(row.values), axis=1)
            dff.drop(columns=cols,inplace=True)
            dff.rename(columns={'mun_regis':'unique_values'}, inplace=True)
            dff = fillMissingMuns(dff, state)
            return dff

def generate_report_state(year, age_range,state, indicator):
    dff = DataDictionaries.mainDF(year, indicator)
    cancDict = DataDictionaries.getCancDict()
    dff = dff.loc[(dff['ent_regis'] == state) & (dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
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

    cols = dff.columns.tolist()
    cols = ['unique_values', 'Organ', 'male', 'female', 'counts']
    curr_count = curr_count[cols]
    curr_count.columns = ['ICD', 'Organ', 'Male Cases', 'Female Cases', 'Total Cases']
    return curr_count


def generate_report_suburst_state(year, age_range, state, indicator):
    dff2 = DataDictionaries.mainDF(year, indicator)
    cancDict = DataDictionaries.getCancDict()
    gender = [1,2]
    result = list()
    for i in gender:
        dff = dff2
        dff = dff.loc[(dff['ent_regis'] == state) & (dff['sexo'] == i)&(dff['edad'] >= age_range[0]) & (dff['edad'] <= age_range[1])]
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


def generate_report_resid(year, state, indicator):
    dff = DataDictionaries.mainDF(year, indicator)
    ent = dff.loc[dff['ent_regis'] == state]
    #NoResid = ent.loc[ent['ent_resid'] != state]
    #Resid = ent.loc[ent['ent_resid'] == state]

    #Resid =  Resid['anio_ocur'].value_counts().rename_axis('unique_values').reset_index(name='counts')
    #NoResid =  NoResid['anio_ocur'].value_counts().rename_axis('unique_values').reset_index(name='counts')

    #new_col = Resid['counts']
    #NoResid.insert(2, column='counts2', value=new_col)
    ent =  ent['month_year_ocurr'].value_counts().rename_axis('unique_values').reset_index(name='counts')
    return ent