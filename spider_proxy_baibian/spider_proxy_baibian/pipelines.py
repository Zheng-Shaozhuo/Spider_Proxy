# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from settings import MYSQL

class SpiderProxyBaibianPipeline(object):
    def process_item(self, item, spider):
        return item


class ProxySqlPipeline(object):
    def __init__(self):
        _host = MYSQL['HOST']
        _port = MYSQL['PORT']
        _user = MYSQL['USER']
        _pass = MYSQL['PASS']
        _db = MYSQL['DB']
        _charset = MYSQL['CHARSET']

        self._conn = pymysql.connect(host=_host, port=_port, user=_user, passwd=_pass, db=_db, charset=_charset)
        self._cursor = self._conn.cursor()
        print('mysql connect successful')

    def process_item(self, item, spider):
        sql = item.get('sql')
        try:
            self._cursor.execute(sql)
            self._conn.commit()
        except:
            print('sql commit error, => ' + sql)

    def close_spider(self, spider):
        self._cursor.close()
        self._conn.close()
