# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


# 将数据插入数据库
# 方法一：同步
class JianshuPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8mb4'
            # mysql相关时，注意utf-8要写'utf8'.
            # 这里因为subjects字段可能有4个字节的符号，所以指定编码为utf8mb4
        }
        # 连接数据库
        # ** dbparams代表关键字参数，传入一个字典，函数会解包，它会把dictionary中所有键值对转换为关键字参数传进去
        self.conn = pymysql.connect(**dbparams)
        # 创建游标,用于执行数据库操作
        self.cursor = self.conn.cursor()
        self._sql = None

    # 写一个sql语句模板
    # @property是python内置的装饰器，会将方法转换为属性，目的是使得传入的参数可以得到校验
    # %s为字符串格式参数占位符
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,article_id,title,content,author,avatar,pub_time,origin_url,word_count,
            read_count,comment_count,like_count,subjects) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # 让游标执行sql语句，注意要传进sql语句里的参数有多个时要放在一个元组中传递，单个则可以直接传递
        self.cursor.execute(self.sql, (item['article_id'], item['title'], item['content'],
                                       item['author'], item['avatar'], item['pub_time'],
                                       item['origin_url'], item['word_count'], item['read_count'],
                                       item['comment_count'], item['like_count'], item['subjects']))
        # 提交当前事务
        self.conn.commit()
        print("已提交sql")
        return item


# 插入数据到数据库
# 方法二：异步（利用scrapy框架的底层twisted框架的adbpai模块实现异步操纵数据库）
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8mb4',
            'cursorclass': cursors.DictCursor
            # 与方法一不同，这里需要指定游标类，否则不知道使用哪个游标

        }
        # 定义连接池，连接数据库.参数一：mysql的驱动;参数二：连接mysql的配置信息
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,article_id,title,content,author,avatar,pub_time,origin_url,word_count,
            read_count,comment_count,like_count,subjects) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # runInteraction()把self.insert_item()变为异步执行函数
        # 参数1：在异步任务中要执行的函数insert_item
        # 参数2：给传递参数item.
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 给defer添加错误处理，self.dbpool.runInteraction(self.insert_item(), item)出错的话,就会调用self.handle_error函数
        defer.addErrback(self.handle_error, item, spider)
        return item

    # 定义一个插入数据的函数
    # 注意：函数insert_item接收的第一个参数是runInteraction()传递的一个Transaction对象，类似cursor，
    # 所以insert_item函数的时候cursor和item的位置不要搞错啦
    def insert_item(self, cursor, item):
        params = (item['article_id'], item['title'], item['content'],
                                       item['author'], item['avatar'], item['pub_time'],
                                       item['origin_url'], item['word_count'], item['read_count'],
                                       item['comment_count'], item['like_count'], item['subjects'])
        cursor.execute(self.sql, params)

    def handle_error(self, error, item, spider):
        print('-' * 20 + '出错啦' + '-' * 20)
        print(error)
        print('-' * 20 + '出错啦' + '-' * 20)
