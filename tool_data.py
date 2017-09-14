#! /usr/bin/python
# -coding:utf-8-*-
"""
Author:iGuo Lily
AIM: 
数据清洗和相同关键词数据拼接
生成需要导入数据库的数据

*备注：
1、关于goodsInfo 和 datetime 及数字ID的替换：
个人认为一张表足够，记录Info的文字和它们的变更日期，方法为去重
数字ID暂时只能想到用在DF中的ID，目前使用存入csv,index = True 再重新读取的方式
2、按关键词循环，注意控制一次文件夹内的文件数量，如果需要每天的数据单独拼接需要再根据日期加上循环
"""
import os
from datetime import timedelta, datetime

import numpy as np
import pandas as pd


def parse_fname_info(fname):
    if 'tmallPrice' not in fname:
        return None

    fnameinfo = fname.replace('.csv','').split('_')
    retailer = fnameinfo[0].replace('Price','')
    date = fnameinfo[1]
    time = fnameinfo[2]
    keyword = fnameinfo[3]
    pagenum = int(fnameinfo[-1])
    finfo = {
        'retailer':retailer,
        'date':date,
        'time':time,
        'keyword':keyword,
        'pagenum':pagenum,
        'fname':fname,
    }
    return finfo


def select_file(group):
    if len(group)>1:
        def _cmp(x):
            """
            choose the one with the closest one to the base time(7:00 a.m.) of that day
            :param x: string, file name
            :return: datetime.timedelta, timedelta with base time
            """
            finfo = parse_fname_info(x)
            date_string = '-'.join([finfo['date'],finfo['time']])
            timevalue = datetime.strptime(date_string,'%Y-%m-%d-%H-%M-%S')
            date_base = '-'.join([finfo['date'],'07-00-00'])
            timebase = datetime.strptime(date_base,'%Y-%m-%d-%H-%M-%S')
            timedelta = abs(timevalue - timebase)
            return timedelta
        return pd.Series(min(group, key=_cmp))
    elif len(group)==1:
        return group


def select_files(dict):

    # all information of data_source files
    info = []
    for fname in os.listdir(dict):
        finfo = parse_fname_info(fname)
        if finfo is None:
            continue
        info.append(finfo)

    df_info = pd.DataFrame(info)

    # summary
    grouped = df_info.groupby(['date','pagenum'])['fname']
    summary = grouped.apply(len)
    # print(summary[summary!=1])

    # select files
    selected_files = grouped.apply(select_file(dict))
    return selected_files


def clean_sales(x):
    if '万' in str(x):
        x = float(x.split('万')[0])*10000
        return int(x)
    else:
        return x


def join_data(dict,key):
    df_selected_files = select_files(dict)

    dfs = []
    for fname in df_selected_files:

        df = pd.read_csv(os.path.join(dict, fname))
        finfo = parse_fname_info(fname)

        df['date'] = finfo['date']
        df['keyword'] = finfo['keyword']
        df['pagenum'] = finfo['pagenum']
        df['order'] = df.index+1
        df['rank'] = (df['pagenum'] - 1) * len(df) + df['order']
        try:
            df.rename(columns={'monthly_sales': 'sales'}, inplace=True)
        except KeyError:
            pass
        df['sales'] = df['sales'].apply(clean_sales)
        dfs.append(df)


    df_final = pd.concat(dfs).sort_values(['date','rank'])
    df_final.to_csv('../data/{}.csv'.format(key),index=False)

    df_goods = pd.DataFrame({'GoodsInfo': df_final['goodsName'],
                  'ChanDate':df_final['date']}).drop_duplicates('date')

    df_goods.to_csv('../goodsInfo/{}.csv'.format(key))

    return df_final


info_dict = {}


# clean & concat
def main():

    CPI_list = pd.read_csv('tmall_keywords.csv')['keyword']
    for key in CPI_list:
        dict = 'E:/CPPdata/keywords/{}'.format(key)
        group = list(os.listdir(dict))
        select_file(group)
        join_data(dict,key)

if __name__=='__main__':
    main()