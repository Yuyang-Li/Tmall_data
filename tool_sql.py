"""
Author:Lily
*备注：
1、建立连接部分为示范代码，运行需要一个具体的服务器
2、此处安装的包为mysqlclient
"""
import pandas as pd
import MySQLdb
# read data
# 先用临时创建的
df_final = pd.DataFrame({'a':[1,2,3,4,5],
       'b':[1,1,2,3,4]})

# connect
con = MySQLdb.connect(
    user = 'scott', password = 'tiger',
    host = '127.0.0.1',
    database = 'employees',
    use_pure = False
)
cur = con.cursor()
con.autocommit()

#创建表：t_tmall_price
tmall_price = 'create table t_tmall_price(' \
      'keyword VARCHAR (45),' \
      'params VARCHAR (45),' \
      'goodsID INT ,' \
      'price DECIMAL(10),' \
      'sales INT, ' \
      'comments INT, ' \
      'datetime DATETIME_INTERVAL_CODE, ' \
      'date DATETIME_INTERVAL_CODE, ' \
      'rank INT, ' \
      'pagenum INT, ' \
      'pageorder INT, ' \
      'goodsInfoID INT, ' \
      'shopInfoID INT, ' \
      'scrapeRule INT, ' \
      'rankMETHOD VARCHAR (1),' \
      'PRIMARY KEY (keyword,params,scrapeRule,rankMETHOD,goodsID,datetime),' \
      'FOREIGN KEY(goodsID) REFERENCES t_tmall_goodsInfo(goodsID))' \
      'FOREIGN KEY (shopInfoID) REFERENCES  t_tmall_shopInfo(shopInfoID)'

goodsInfo = 'create table t_tmall_goodsInfo(' \
            'goodsInfoID INT ' \
            'goodsID INT ' \
            'goodsName VARCHAR(45) ' \
            'goodsInfoTimeID INT ' \
            'PRIMARY KEY (goodsInfoID))'

shopInfo = 'create table t_tmall_shopInfo(' \
           'shopInfoID INT ' \
           'shopID INT ' \
           'shopName VARCHAR (45)' \
           'shopInfoTimeID INT ' \
           'PRIMARY KEY (shopInfoID))'

cur.execute(tmall_price)
cur.execute(goodsInfo)
cur.execute(shopInfo)


def insert(line):
    """将想录入的列代替‘a’的位置
    调整Dataframe中各列输入的顺序和创建表的变量顺序相同，按行批量写入数据
    """
    line = list(df_final['a'])
    cur.execute('insert into t_tmall_price values(%s,%s,%s)', line)

df_final.apply(insert,axis = 1)

cur.close()
con.close()


df = pd.DataFrame({'A':[1,2,3]})
df.to_sql()