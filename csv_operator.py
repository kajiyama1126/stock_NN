import copy
import os
import shutil

import numpy as np
import pandas as pd


def copy_file_size_select(size, name, place, to_place):
    os.chdir(place)
    try:
        os.makedirs(to_place)
    except:
        pass
    if os.path.getsize(name) > size:
        shutil.copyfile(place + '\\' + name, to_place + '\\' + name)


# 0Kbのファイルを除いてコピー(place⇨to_place)
def except0KB(place, to_place):
    directory = os.listdir(place)
    for name in directory:
        copy_file_size_select(100, name, place, to_place)
    print('finish_except0KB')


# 列名を英語に変更
def column_rename(place, to_place, add_name):
    os.chdir(place)
    directory = os.listdir(place)
    for name in directory:
        data = pd.read_csv(name, encoding='cp932')
        # print(data.columns)
        data.columns = ["code", 'type', 'market', 'start', 'high', 'low', 'last', 'number of sale', 'money of sale']
        data.index = data["code"]
        data = data.drop("code", axis=1)
        data = data.dropna()
        os.chdir(to_place)
        rename = name.rstrip('.csv') + add_name + '.csv'
        data.to_csv(rename)
        os.chdir(place)
    print('finish_column_rename')


# 株価データを数日分結合
def connect_some_days(days, place):
    folder_name = 'stock_data_for' + str(days) + 'days'
    os.chdir('/Users/kajiyama/PycharmProjects/stock_NN/stock_data')
    try:
        os.mkdir(folder_name)
    except:
        pass
    directory = os.listdir(place)
    os.chdir(place)
    for i in range(len(directory) - days + 1):
        base_data = pd.DataFrame()
        for j in range(days):
            data = pd.read_csv(directory[i + j], encoding='cp932', index_col='code')
            if j != 0:
                data = data.drop(['type', 'market'], axis=1)
                data.columns = ['start' + str(j), 'high' + str(j), 'low' + str(j), 'last' + str(j),
                                'number of sale' + str(j), 'money of sale' + str(j)]
            base_data = pd.concat([base_data, data], axis=1)
        base_data = base_data.dropna()
        filename = directory[i].rstrip('.csv') + 'for' + str(days) + 'days.csv'
        os.chdir('/Users/kajiyama/PycharmProjects/stock_NN/stock_data/' + folder_name)
        base_data.to_csv(filename)
        os.chdir(place)
    print('finish_connect_some_days')


# 初日の始値をもとに上昇率に変換
def base_transform(days):
    basename = ['start', 'high', 'low', 'last']
    column_name = copy.copy(basename)
    os.chdir('/Users/kajiyama/PycharmProjects/stock_NN/stock_data')
    folder_name = 'stock_data_for' + str(days) + 'days_reform'
    try:
        os.mkdir(folder_name)
    except:
        pass
    place = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/'+'stock_data_for' + str(days)+'days'
    to_place = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/'+folder_name
    for i in range(days - 1):
        for j in basename:
            column_name.append(j + str(i + 1))
    os.chdir(place)
    directory = os.listdir(place)
    # name = directory[0]
    for name in directory:
        data = pd.read_csv(name, encoding='cp932', index_col=0)
        # data = data.set_index(data.iloc[:,0])
        # print(data)
        start = copy.copy(data['start'].values)
        # print(start)
        for i in range(len(column_name)):
            data[column_name[i]] = (data[column_name[i]] / start - 1.0)
        rename = name.rstrip('.csv') + '_reform.csv'
        os.chdir(to_place)
        data.to_csv(rename)
        os.chdir(place)
    print('finish_base_transform')


# 教師データを作成（(上昇率/パーセント)を4捨5入）
def make_teacher_data(place, percent):
    to_place = 'stock_data_teacher'
    place0 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data'
    os.chdir(place0)
    try:
        os.mkdir('stock_data_teacher')
    except:
        pass
    os.chdir(to_place)
    directory = os.listdir(place)
    for name in directory:
        os.chdir(place)
        data = pd.read_csv(name, encoding='cp932', index_col='code')
        data = data.drop(['type', 'market', 'number of sale', 'money of sale'], axis=1)
        column_name = ['teacher_start', 'teacher_high', 'teacher_low', 'teacher_last']
        data.columns = column_name
        start = copy.copy(data['teacher_start'].values)

        for i in range(len(column_name)):
            data[column_name[i]] = (data[column_name[i]] / start - 1.0)
        data['teacher_only_up_down'] = np.sign(copy.copy(data['teacher_last'].values))
        data['teacher_' + str(percent)] = np.round((copy.copy(data['teacher_last'].values) * 100) / percent)
        os.chdir(place0)
        os.chdir(to_place)
        rename = name.rstrip('.csv') + '_teacher.csv'
        data.to_csv(rename)
    print('finish_make_teacher_data')

# 教師データと上昇率のデータを合成
def connect_data(teacher_place, to_place, days):
    place = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/'+'stock_data_for' + str(days) + 'days_reform'
    os.chdir(place)
    directory = os.listdir(place)
    teacher_directory = os.listdir(teacher_place)
    i = 0
    for name in directory:
        os.chdir(place)
        data = pd.read_csv(name, encoding='cp932', index_col=0)
        os.chdir(teacher_place)
        if i + days > len(teacher_directory) - 1:
            print('finish_connect_data')
            return
        teacher_name = teacher_directory[i + days]
        teacher_data = pd.read_csv(teacher_name, encoding='cp932', index_col=0)
        data = pd.concat([data, teacher_data], axis=1)
        data = data.dropna()
        os.chdir(to_place)
        rename = name.rstrip('.csv') + 'connect.csv'
        data.to_csv(rename)
        i += 1
    print('finish_connect_data')


place0 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data'
place = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/download_stock_data_test'
place1 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_except0KB'
place2 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/column_rename'
place3 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_for2days'
place4 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_for2days_reform'
place5 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_teacher'
place6 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/connect'
add = 'column_rename'

days = 5
percent = 2

except0KB(place, place1)

column_rename(place1, place2, add)

connect_some_days(days, place2)
base_transform(days)
make_teacher_data(place2, percent)
connect_data(place5, place6, days)
