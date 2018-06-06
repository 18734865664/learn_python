#! /usr/local/python3/bin/python3
# encoding: utf-8

import pymysql

mysql_host = "10.100.137.179"
mysql_user = "root"
mysql_pass = '123123'
mysql_port = 3306

# 实例化mysql
# 假定testdb库已经存在，指定db参数，也可以不指
# db = pymysql.connect(host = mysql_host, user = mysql_user, passwd = mysql_pass, charset = "utf8", port = mysql_port, db = "testdb")
db = pymysql.connect(host = mysql_host, user = mysql_user, passwd = mysql_pass, charset = "utf8", port = mysql_port,)

# 创建游标对象cursor
cursor = db.cursor()

# 查询
sql = "show databases"
cursor.execute(sql)

# fetchnoe() 获取下一个查询结果 
# while True:
#     data = cursor.fetchone()
#     if data:
#         print(data)
#     else:
#         break
    

# fetchall()获取所有结果
data = cursor.fetchall()
print(data)

# 对于支持事务的数据库， 在Python数据库编程中，当游标建立之时，就自动开始了一个隐形的数据库事务。
# commit()方法游标的所有更新操作，rollback（）方法回滚当前游标的所有操作。每一个方法都开始了一个新的事务。


