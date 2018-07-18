# -*- coding: utf-8 -*-
import scrapy
import time

from ..items import SpiderSqlItem


class IpbuSpider(scrapy.Spider):
    name = 'ipbu'
    allowed_domains = ['89ip.cn']
    api_url = 'http://www.89ip.cn/apijk/?&tqsl=9999&sxa=&sxb=&tta=&ports=&ktip=&cf=1'

    def parse(self, response):
        try:
            _buff = '%s' % response.text
            _start = _buff.find('<br/>') + 7
            _end = _buff.find('<br>')
            ip_list = _buff[_start : _end].split('<BR>')

            sql = 'insert into proxies(ip, port, valid, memo, last_check_timestamp, created_at) values'
            for ip in ip_list:
                ip_params = ip.split(':')
                sql += "('%s', %d, 0, 'http://www.89ip.cn', 0, %d)," % (ip_params[0], int(ip_params[1]), int(time.time()))
            sql = sql.strip(',')
            item = SpiderSqlItem()
            item['sql'] = sql
            yield item
        except:
            print('get page content error.')
        pass

    def start_requests(self):
        yield scrapy.Request(url=self.api_url, meta={'referer': 'http://www.89ip.cn'})

