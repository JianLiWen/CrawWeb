# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import cursors
import logging
from twisted.enterprise import adbapi
import time
import copy
class CrawwebPipeline(object):
    # 函数初始化
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        """类方法，只加载一次，数据库初始化"""
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        # 返回一个pipeline对象
        return cls(db_pool)

    def process_item(self, item, spider):
        """
               数据处理
               :param item:
               :param spider:
               :return:
               """
        myItem = {}
        myItem["question"] = item["question"]
        myItem["answer"] = item["answer"]
        logging.warning(myItem)
        # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
        asynItem = copy.deepcopy(myItem)

        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, asynItem)

        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, myItem, spider)
        return myItem

        # 处理sql函数

    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO Niuke (question,answer) VALUES ('{}','{}')".format(
            item['question'], item['answer'])
        # 执行sql语句
        cursor.execute(sql)
        # 错误函数

    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print("failure", failure)
