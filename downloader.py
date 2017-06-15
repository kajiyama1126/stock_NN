#-*- coding:utf-8 -*-
import urllib.request
import os
import shutil
from time import sleep
import  sys

def download(url,name,place):
    urllib.request.urlretrieve(url, name+'.csv')

def copy_file_size_select(size, name, place, to_place):
    os.chdir(place)
    try:
        os.makedirs(to_place)
    except:
        pass
    if os.path.getsize(name) > size:
        shutil.copyfile(place + '\\' + name, to_place + '\\' + name)


name = '2015-09-03'
url = 'http://k-db.com/stocks/'+name+'?download=csv'
place = 'stockdata'

# years=['2015','2016','2017']
years=['2010','2011','2012','2013','2014','2015','2016','2017']
months = [str(i+1).zfill(2) for i in range(12)]
days = [str(i+1).zfill(2) for i in range(31)]
print(months)
# dates = []
# for i in range()
#
# place = 'Users/kajiyama/PycharmProjects/stock_NN/stock_data/download_stock_data'
# to_place = 'Users/kajiyama/PycharmProjects/stock_NN/stock_data/stock_data_except0KB'
home_place = 'D:\Pycharm Project\stock_NN\stock_data\download_stock_data'
# for year in years:
#     for month in months:
#         for day in days:
#             copy_file_size_select(1000,year+'-'+month+'-'+day+'.csv',place,to_place)

# os.chdir(place)
os.chdir(home_place)
for year in years:
    for month in months:
        for day in days:
            file_name = year+'-'+month+'-'+day+'.csv'
            if os.path.isfile(file_name):
                pass
            else:
                for i in range(10):
                    try:
                        name = year+'-'+month+'-'+day
                        url = 'http://k-db.com/stocks/' + name + '?download=csv'
                        print(name)
                        sleep(10)
                        download(url, name, place)
                        break
                    except urllib.error.HTTPError:
                        print('HTTPError')
                        sleep(120)
