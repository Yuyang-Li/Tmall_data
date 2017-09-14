"""
date:2017_04_24
Author: Lily
sorting index and moving the files into the right places

输入：
①起、始日期（年月日）（在最底部）
②月份（最顶端的Index一项）

*备注：
1、name_list 为目前储存了数据的服务器
还在使用中的有：
'ZhangGuo', 'HaoZedong',  'QiBin', 
'XieTie','YuBin', 'ZhangYilin','FSOL'
2、run的时候会print来源和目标文件夹用于检查，如果目标文件夹为空将print "None"
3、地址路径若有改变，请记得修改地址
4、使用时为了确保每个月有自己的文件夹，
"""
#-*- coding: utf-8 -*-    # import system default encoding

import datetime
import os

Index = 'H:/CPPdata/TmallData_2017-08'
name_list = ['ZhangGuo', 'HaoZedong', 'LiuXiaoman', 'QiBin', 'XieTie',
             'YouYuchao', 'YuBin', 'YuXinhui',
             'ZhangYilin','FSOL']


# move files in old to new
def move_file(old,new):
    if os.path.exists(old):
        if not os.path.exists(new):
            os.makedirs(new)
        for i in os.listdir(old):
            try:
                old_fname = os.path.join(old,i)
                new_fname = os.path.join(new,i)
                if not os.path.isfile(new_fname):
                    os.rename(old_fname,new_fname)
            except OSError:
                print(i)
    else:
        print('none')


def create_path(index_old,index_new,y1,m1,d1,y2,m2,d2):
    begin = datetime.date(
        y1,m1,d1)
    end = datetime.date(y2,m2,d2)
    for i in range((end-begin).days+1):
        date = begin + datetime.timedelta(days = i)
        old = '{}/TmallData_{}'.format(index_old,str(date))
        new = '{}/TmallData_{}'.format(index_new,str(date))
        print (old, 'to', new)
        move_file(old,new)

# join several data files into one by keywords

def main():
    for name in name_list:
        file = 'H:/Web_Data_3_31/{}/Data/TmallData'.format(name)
        create_path(file,Index,2017,8,9,2017,8,18)


if __name__ == '__main__':
    main()