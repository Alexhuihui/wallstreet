# -*- coding:utf-8 -*-
import pymysql
import time


class Dao(object):
    def get_conn(self):
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="QWErty123", db="wallstreet",
                               charset="utf8")

        return conn

    def insert(self, contents):
        createtimes = str(time.time())
        insert_sql = "insert into information(content, createtime) values('%s', '%s' ) " % (contents, createtimes)
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute(insert_sql)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        cur.close()
        conn.close()

    def delete(self):
        pass

    def update(self):
        update_sql = "update information set status = 1 where status = 0"
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute(update_sql)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        cur.close()
        conn.close()

    def select(self):
        select_sql = "select content from information where status = 0"
        content = ""
        list = []
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute(select_sql)
            rs = cur.fetchall()
            for line in rs:
                list.append(line)
            for i in range(0, list.__len__()):
                list[i] = str(list[i])
            content = '\n'.join(list)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        cur.close()
        conn.close()
        self.update()
        return content


if __name__ == '__main__':
    dao = Dao()
    print(dao.select())
