# -*- coding: utf-8 -*-
from time import time

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SpiderSqlItem

# class KuaidailiSpider(scrapy.Spider):
#     name = 'kuaidaili'
#     allowed_domains = ['kuaidaili.com']
#     start_urls = ['http://kuaidaili.com/']
#
#     def parse(self, response):
#         pass



class KuaidailiSpider(CrawlSpider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/', 'https://www.kuaidaili.com/free/intr/']
    rules = (
        Rule(LinkExtractor(allow='/free/intr/\d+/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow='/free/inha/\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            insert_sql = "insert into proxies(ip, port, valid, memo, last_check_timestamp, created_at) values"
            for tr in response.css('#list > table > tbody > tr'):
                _ip = tr.css('td:nth-child(1)::text').extract_first()
                _port = tr.css('td:nth-child(2)::text').extract_first()
                _type = tr.css('td:nth-child(3)::text').extract_first()
                _protocol = tr.css('td:nth-child(4)::text').extract_first()
                _location = tr.css('td:nth-child(5)::text').extract_first()
                _answer = tr.css('td:nth-child(6)::text').extract_first()
                _last_check = tr.css('td:nth-child(7)::text').extract_first()
                memo = _protocol + ' | ' + _type + ' | ' + _location + ' | ' + _answer + ' | ' + _last_check + ' | kuaidaili.com'
                insert_sql = insert_sql + ("('%s', %d, 0, '%s', 0, %d)," % (_ip, int(_port), memo, int(time())))

            item = SpiderSqlItem()
            item['sql'] = insert_sql.strip(',')
            yield item
        except:
            print('curr page parse td error')
