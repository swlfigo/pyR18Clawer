# -*- coding:utf-8 -*-
import sqlite3
import time


#单例模式
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


#数据库记录类
@singleton
class VMDBMangaer(object):

    dbName = 'r18InfomationClawer.db'

    def __init__(self):
        self.initDataBase()
        pass

    def initDataBase(self):
        print('DB Manager Init')

        # 连接到SQLite数据库
        # 数据库文件是videoClawer.db
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect(self.dbName)

        # 创建一个Cursor
        curs = conn.cursor()

        # 创建一个表
        # 存在跳过
        curs.execute('''
        CREATE TABLE IF NOT EXISTS r18InfoTable(
        id          INTEGER           PRIMARY KEY     AUTOINCREMENT,
        name        TEXT,
        localCover       TEXT,
        remoteCover   TEXT,
        publishDate  TEXT,
        videoInfo TEXT
        )''')

        curs.close()
        conn.commit()
        conn.close()


#传入执行命令数组
    def execute(self,executeString):
        fetchResult = []
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()

        try:
            results = cursor.execute(executeString)
            fetchResult = results.fetchall();
            print('执行成功')
        except Exception as e:
            print('命令错误', e)
            pass

        cursor.close()
        conn.commit()
        conn.close()
        return fetchResult

    #记录数据
    #传进是一个数组
    #titleName, publishDate, videoInfo, remotecover, localcover
    #publishDate需要改格式
    def startRecord(self, infoList):
        if infoList is None:
            return

        # 连接数据库
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        # 更新或者写入数据库
        sql_cmd = ''' SELECT * FROM r18InfoTable where NAME = '%s' ''' % infoList[0]
        cursor.execute(sql_cmd)
        res = cursor.fetchall()
        date = str((time.localtime())[0]) + '-' + str(infoList[1])

        # print(infoList[2])

        if len(res) > 0:
            # 存在数据，更新
            sql_updateCMD = ''' update r18InfoTable set localCover = '%s' , remoteCover = '%s' , publishDate = '%s', videoInfo = '%s' WHERE NAME  = '%s' ''' %(infoList[4], infoList[3] , date , infoList[2] , infoList[0])
            try:

                cursor.execute(sql_updateCMD)
                print('更新数据成功!!!')
            except Exception as e:
                # 更新失败
                print('更新失败', e)

        else:
            # 不存在，写入
            try:
                # titleName, publishDate, videoInfo, remotecover, localcover
                sql = "insert into r18InfoTable (name,localCover,remoteCover,publishDate,videoInfo) values " \
                      "('%s','%s','%s','%s','%s')" % (
                      infoList[0], infoList[4], infoList[3], date, infoList[2])
                cursor.execute(sql)
                print('写入数据成功!!!')
            except Exception as e:
                # 写入失败
                print('写入错误', e)


        cursor.close()
        conn.commit()
        conn.close()


    #执行命令
    def execute(self, executeString):
        fetchResult = []
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()

        try:
            results = cursor.execute(executeString)
            fetchResult = results.fetchall();
            print('执行成功')
        except Exception as e:
            print('命令错误', e)
            pass

        cursor.close()
        conn.commit()
        conn.close()

        return fetchResult