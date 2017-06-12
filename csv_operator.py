import os
import shutil
import codecs
import pandas as pd
import datetime
import copy


def copy_file_size_select(size, name, place, to_place):
    os.chdir(place)
    try:
        os.makedirs(to_place)
    except:
        pass
    if os.path.getsize(name) > size:
        shutil.copyfile(place + '\\' + name, to_place + '\\' + name)

def except0KB(place, to_place):#0Kbのファイルを除いてコピー(place⇨to_place)
    directory = os.listdir(place)
    for name in directory:
        copy_file_size_select(100, name, place, to_place)

def column_rename(place,to_place,add_name):
    os.chdir(place)
    directory = os.listdir(place)
    for name in directory:
        data = pd.read_csv(name,encoding='cp932')
        print(data.columns)
        data.columns = ["code",'type','market','start','high','low','last','number of sale', 'money of sale']
        data.index =  data["code"]
        data = data.drop("code", axis = 1)
        data = data.dropna()
        os.chdir(to_place)
        rename = name.rstrip('.csv') + add_name+'.csv'
        data.to_csv(rename)
        os.chdir(place)

def connect_some_days(days, place):#株価データを数日分結合
    folder_name = 'stock_data_for' + str(days) + 'days'
    os.chdir('/Users/kajiyama/PycharmProjects/stock_NN/stock_data')
    try:
        os.mkdir(folder_name)
    except:
        pass
    directory = os.listdir(place)
    os.chdir(place)
    for i in range(len(directory)-days+1):
        base_data = pd.DataFrame()
        for j in range(days):
            data = pd.read_csv(directory[i+j], encoding='cp932', index_col='code')
            if j != 0:
                data = data.drop(['type','market'], axis=1)
                data.columns = ['start'+str(j), 'high'+str(j), 'low'+str(j), 'last'+str(j), 'number of sale'+str(j), 'money of sale'+str(j)]
            base_data = pd.concat([base_data,data],axis=1)
        base_data = base_data.dropna()
        filename = directory[i].rstrip('.csv') + 'for' + str(days) + 'days.csv'
        os.chdir('/Users/kajiyama/PycharmProjects/stock_NN/stock_data/'+folder_name)
        base_data.to_csv(filename)
        os.chdir(place)



def base_transform(place,to_place,days):
    basename = ['start','high','low','last']
    column_name = copy.copy(basename)
    for i in range(days-1):
        for j in basename:
            column_name.append(j+str(i+1))
    os.chdir(place)
    directory =os.listdir(place)
    # name = directory[0]
    for name in directory:
        data = pd.read_csv(name, encoding='cp932')
    # print(data)
        start = copy.copy(data['start'].values)
    # print(start)
        for i in range(len(column_name)):
            data[column_name[i]] = (data[column_name[i]]/start -1.0)
        rename = name.rstrip('.csv') + '_reform.csv'
        os.chdir(to_place)
        data.to_csv(rename)
        os.chdir(place)






place = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/download_stock_data_test'
place1 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_except0KB'
place2 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/column_rename'
place3 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_for2days'
place4 = '/Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_for2days_reform'
add = 'column_rename'


# except0KB(place,to_place)

# column_rename(to_place,to_place2,add)

# connect_some_days(3,to_place2)
base_transform(place3,place4,2)