#-*- coding: utf-8 -*-
import pymysql
DB_NAME = 'hebeiaqi'
TABLE_NAME = 'Citys'
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '900911',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
    }


def addcitys(sqls):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db(DB_NAME)
    cursor = conn.cursor()


    try:
        # 执行一条insert语句，返回受影响的行数

        # 执行多次insert并返回受影响的行数
        cursor.execute("INSERT INTO Citys (CityName ,DataTime ,AQI ,Level ,Type ,LevelIndex ,MaxPoll ,Intro ,Tips,PM25 , PM10 , SO2, CO, NO2 , O38H ,O31H ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",sqls)
        # cursor.executemany("INSERT INTO Citys (CityName ,DataTime ,AQI ,Level ,Type ,LevelIndex ,MaxPoll ,Intro ,Tips) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);",sqls)

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


def addRegion(sql):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db(DB_NAME)
    cursor = conn.cursor()

    try:
        # 执行一条insert语句，返回受影响的行数

        # 执行多次insert并返回受影响的行数
        cursor.execute(
            "INSERT INTO Region (CityName ,Region,Site,DataTime ,AQI ,Level ,LevelIndex ,MaxPoll ,Intro ,Tips, CLng,CLat,PM25 , PM10 , SO2, CO, NO2 , O38H ,O31H ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",sql)
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

def adddaycitys(sql):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db(DB_NAME)
    cursor = conn.cursor()

    try:
        # 执行一条insert语句，返回受影响的行数

        # 执行多次insert并返回受影响的行数
        cursor.execute(
            "INSERT INTO daycitys (CityName ,DataTime ,AQI ,Level ,LevelIndex ,MaxPoll ,Intro ,Tips ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);", sql)
        # cursor.executemany("INSERT INTO Citys (CityName ,DataTime ,AQI ,Level ,Type ,LevelIndex ,MaxPoll ,Intro ,Tips) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);",sqls)

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


def adddayRegion(sql):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db(DB_NAME)
    cursor = conn.cursor()

    try:
        # 执行一条insert语句，返回受影响的行数

        # 执行多次insert并返回受影响的行数
        cursor.execute(
            "INSERT INTO dayregion (cid ,Site,DataTime ,AQI ,Level ,LevelIndex ,MaxPoll ,Intro ,Tips, CLng,CLat ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            sql)
        # cursor.executemany("INSERT INTO Citys (CityName ,DataTime ,AQI ,Level ,Type ,LevelIndex ,MaxPoll ,Intro ,Tips) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);",sqls)

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




def addRegion(sql):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db(DB_NAME)
    cursor = conn.cursor()

    try:
        # 执行一条insert语句，返回受影响的行数

        # 执行多次insert并返回受影响的行数
        cursor.execute(
            "INSERT INTO Region (CityName ,Region,Site,DataTime ,AQI ,Level ,LevelIndex ,MaxPoll ,Intro ,Tips, CLng,CLat,PM25 , PM10 , SO2, CO, NO2 , O38H ,O31H ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",sql)
        # 提交执行
        conn.commit()
        print(cursor.lastrowid)
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

    pass
# try:
#
#     conn = pymysql.connect(**config)
#     conn.autocommit(1)
#
#     cursor = conn.cursor()
#     # 创建数据库
#     DB_NAME = 'hebeiaqi'
#     cursor.execute('DROP DATABASE IF EXISTS %s' % DB_NAME)
#     cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)
#     conn.select_db(DB_NAME)
#      #创建表
#     TABLE_NAME = 'Citys'
#     cursor.execute('CREATE TABLE %s(id int primary key auto_increment,CityName varchar(30),DataTime datetime,AQI varchar(30),Level varchar(30),Type varchar(30),LevelIndex varchar(30),MaxPoll varchar(30),Intro varchar(30),Tips varchar(30),PM25 varchar(30), PM10 varchar(30), SO2 varchar(30), CO varchar(30), NO2 varchar(30), O38H varchar(30), O31H varchar(30))'%TABLE_NAME)
#
# except:
#     import traceback
#
#     traceback.print_exc()
#     # 发生错误时会滚
#     conn.rollback()
# finally:
#     # 关闭游标连接
#     cursor.close()
#     # 关闭数据库连接
#     conn.close()



