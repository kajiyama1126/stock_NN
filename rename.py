# -*- coding:utf-8 -*-
import os
import shutil
import time
import urllib
import urllib.request
home_place = 'D:\Pycharm Project\stock_NN\stock_data_separate'
home_place2 = 'D:\Pycharm Project\stock_NN\stock_data_separate_2'
os.chdir(home_place)
name = os.listdir(home_place)
# os.chdir(home_place2)

for file in name:
    base_name = file
    # rename = file.rstrip('.csv')
    rename = base_name +'.csv'
    os.rename(base_name,rename)