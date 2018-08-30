import pymysql
import copy
a={1:[1,'男']}
for i in a:
    if a[i]==[1,'男']:
        print(i)

MysqlDatabase = pymysql.connect(host='192.168.7.31',port=3306,user='ngoss_dim',passwd='ngoss_dim')
MysqlCursor=MysqlDatabase.cursor()
UseDatabase='label_support'
MysqlCommand = "select BatchMap,ClassifyValueMap from %s.ResultPersonNumber;" % UseDatabase
MysqlCursor.execute(MysqlCommand)
BatchAndValueMapTupleList = MysqlCursor.fetchall()
print(BatchAndValueMapTupleList)