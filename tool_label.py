"""
Author: Lily
AIM:
按关键词筛选数据文件到同一文件夹
CPI列表来源：晓曼、星宇学长整理
关键词来源：最底层关键词

输入：起、始日期（年月日）

*备注：
1、用“-”分隔的关键词被切分为两个词，合并到第一个词所在的文件夹
2、速度非常慢，每成功一个文件夹都会print两次Success
3、可以用于查找单一的关键词
"""

import os
import datetime
import pandas as pd


def find_key(key,y1,m1,d1,y2,m2,d2):
    begin = datetime.date(y1, m1, d1)
    end = datetime.date(y2, m2, d2)
    for i in range((end - begin).days + 1):
        date = begin + datetime.timedelta(days=i)
        source = 'E:/CPPdata/TmallData_2017-06/TmallData_{}'.format(str(date))
        target = 'E:/CPPdata/keywords/{}'.format(key)
        print('running')
        list = os.listdir(source)
        print('running')
        if not os.path.isdir(target):
            os.makedirs(target)
        for f in list:
            if key in f:
                old = os.path.join(source,f)
                new = os.path.join(target,f)
                open(new, "wb").write(open(old, "rb").read())
                csv_new = '{}.csv'.format(new)
                os.rename(new,csv_new)
                if os.path.isfile(csv_new):
                    print ("Success")
                else:
                    raise IOError

def main():
    CPI_list = pd.read_csv('tmall_keywords.csv')['keyword']
    for key in CPI_list:
        if '-' in key:
            k1 = key.split('-')[0]
            k2 = key.split('-')[1]
            find_key(k1,2017,3,31,2017,8,31)
            find_key(k1,2017,3,31,2017,8,31)
            print('Warning:{} == {}'.format(k1,k2))
        else:
            find_key(key,2017,3,31,2017,8,31)

if __name__ == '__main__':
    main()