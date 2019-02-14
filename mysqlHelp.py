#-*- coding: utf-8 -*-
import pymysql
DB_NAME = 'hebeiaqi'
TABLE_NAME = 'Citys'
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
    }

def addcrow(str,sql):
    #str sql语句 sql  值
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db(DB_NAME)
    cursor = conn.cursor()

    try:
        # 执行一条insert语句，返回受影响的行数   cursor.executemany()多条
        cursor.execute(str, sql)
        # 提交执行
        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        # 如果执行sql语句出现问题，则执行回滚操作

        conn.rollback()
        print(e)
    finally:
        # 不论try中的代码是否抛出异常，这里都会执行
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()



