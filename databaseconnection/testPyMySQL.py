# -*- coding:utf-8 -*-
from databaseconnection import dao
import pymysql

dao = dao.Dao()
print(dao.select_once_data())
# conn = dao1.get_conn()
#
# cur = conn.cursor()
# insert_sql1 = "insert into information(id, content) VALUES(1, 'hello') "
# insert_sql2 = "insert into information(id, content) VALUES(2, 'world') "
#
# update_sql1 = "update information set content = '汪永晖' where id = 2"
#
# delete_sql = "delete from information where id = 2"

# dao.insert("qqqqq")