import os
import numpy as np
import pandas as pd
import copy

def column_rename(place, to_place, add_name):
    os.chdir(place)
    directory = os.listdir(place)
    sequence = np.array

    for name in directory:
        data = pd.read_csv(name, encoding='cp932')
        # print(data.columns)
        data.columns = ['date','time', 'start', 'high', 'low', 'last', 'numbers', 'money']
        # data.index = data["code"]
        data = data.drop("date", axis=1)
        data = data.dropna()
        seq = len(data.index)
        data['sequence'] = np.array([int(seq - i) for i in range(seq)])
        os.chdir(to_place)
        rename = name.rstrip('.csv') + add_name + '.csv'
        data.to_csv(rename)
        os.chdir(place)
    print('finish_column_rename')

def time_sort(place,to_place,add_name):
    os.chdir(place)
    directory = os.listdir(place)
    for name in directory:
        data = pd.read_csv(name, encoding='cp932',index_col='sequence')
        # data.sort_values(by='time')
        data = data.sort_index()
        rename = name.rstrip('.csv') + add_name + '.csv'
        os.chdir(to_place)
        data.to_csv(rename)
        os.chdir(place)
        # print(data.columns)

def add_column(place,to_place,add_name):
    os.chdir(place)
    directory = os.listdir(place)
    for name in directory:
        data = pd.read_csv(name, encoding='cp932',index_col='sequence')
        high = data.high
        low = data.low
        data['range'] = high-low

        data = variation(data)
        rename = name.rstrip('.csv') + add_name + '.csv'
        os.chdir(to_place)
        data.to_csv(rename)
        os.chdir(place)

def variation(data):
    index_len = len(data.index)
    column_name =  ['start', 'high', 'low', 'last']
    for name in column_name:
        data_column = np.array(data[name])
        tmp = []
        for i in range(int(index_len)):
            if i == 0:
                tmp.append(0)
            else:
                tmp.append((data_column[i]-data_column[int(i-1)])/data_column[int(i-1)])
        rename = name + '_variation'
        data[rename] = tmp

    return data

if __name__ == '__main__':
    direct = 'D:\Pycharm Project\stock_NN\ptest'
    to_direct = 'D:\Pycharm Project\stock_NN\ptest1'
    to_direct2= 'D:\Pycharm Project\stock_NN\ptest2'
    to_direct3 = 'D:\Pycharm Project\stock_NN\ptest3'
    to_direct4= 'D:\Pycharm Project\stock_NN\ptest4'
    # column_rename(direct,to_direct,'re')
    # time_sort(to_direct,to_direct2,'sort')
    add_column(to_direct2,to_direct3,'add')