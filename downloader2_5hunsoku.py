# -*- coding:utf-8 -*-
import os
import time
import urllib
import urllib.request


def download(site_url, name):
    urllib.request.urlretrieve(site_url, name)


# TOPIX_CORE30
def make_topix_core30():
    code = []
    topix = [2914, 3382, 4063, 4502, 4503, 6501, 6752, 6758, 6861, 6902, 6954, 6981, 7201, 7203, 7267, 7751, 8031,
             8058, 8306, 8316, 8411, 8766, 8801, 8802, 9020, 9022, 9432, 9433, 9437, 9984]
    for i in topix:
        code.append(str(i) + '-T')
    return code


# TOPIX_100
def make_topix_core100():
    code = []
    topix30 = [2914, 3382, 4063, 4502, 4503, 6501, 6752, 6758, 6861, 6902, 6954, 6981, 7201, 7203, 7267, 7751, 8031,
               8058, 8306, 8316, 8411, 8766, 8801, 8802, 9020, 9022, 9432, 9433, 9437, 9984]
    topix70 = [1605, 1878, 1925, 1928, 2502, 2503, 2802, 3402, 3407, 4188, 4452, 4507, 4523, 4528, 4568, 4578, 4661,
               4755, 4901,
               4911, 5020, 5108, 5401, 5411, 5713, 5802, 6273, 6301, 6326, 6367, 6502, 6503, 6594, 6702, 6971, 6988,
               7011, 7186,
               7202, 7261, 7269, 7270, 7741, 7974, 8001, 8002, 8035, 8053, 8113, 8267, 8308, 8309, 8591, 8601, 8604,
               8630, 8725,
               8750, 8795, 8830, 9021, 9064, 9201, 9202, 9502, 9503, 9531, 9532, 9735, 9983]
    topix100 = topix30 + topix70
    for i in topix100:
        code.append(str(i) + '-T')

    return code


#############################################################################################################
# 変更可能!

# 欲しいデータの日付'yyyymmdd'で記入
# 本日含め4日間取得可能(サイトの都合)
days = ['20171006']

# ダウンロードする銘柄を記入([OOOO-T, ...,]の形)
# 上の関数は一例(topix_core30,topix100)
names = make_topix_core100()

# 保存場所を選択(任意)
home_place = 'D:\Pycharm Project\stock_NN\stock_data_5hunsoku'

###########################################################################################################

if __name__ == '__main__':
    #フォルダの存在確認（なかったら作成）
    if not os.path.isdir(home_place):
        os.mkdir(home_place)

    os.chdir(home_place)
    for code_name in names:
        for day in days:
            # code + days + .csvで保存
            file_name = code_name + day + '.csv'
            # 同じファイル名があれば保存しない
            if os.path.isfile(file_name):
                pass
            else:
                for i in range(10):
                    try:
                        # urlのサイトにアクセス
                        url = 'http://k-db.com/stocks/' + code_name + '/5m/' + day + '?download=csv'
                        print(day, code_name)
                        # 連続でサーバーにアクセスしないため10sec()
                        time.sleep(10)
                        download(url, file_name)
                        break

                    # download失敗したとき120sec開けてリトライ
                    except urllib.error.HTTPError:
                        print('HTTPError')
                        time.sleep(120)
