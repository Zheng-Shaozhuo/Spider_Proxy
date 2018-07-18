# -*- coding: utf-8 -*-
import urlparse

import scrapy
import time

from ..items import SpiderSqlItem


class Swei360Spider(scrapy.Spider):
    name = 'swei'
    allowed_domains = ['swei360.com']
    start_urls = ['http://www.swei360.com/free/?stype=1&page=1', 'http://www.swei360.com/free/?stype=2&page=1',
                  'http://www.swei360.com/free/?stype=3&page=1', 'http://www.swei360.com/free/?stype=4&page=1']

    def parse(self, response):
        try:
	    curr_time = int(time.time())
            sql = 'insert into proxies(ip, port, valid, memo, last_check_timestamp, created_at) values'
            for tr in response.css('#list > table > tbody > tr'):
                ip = tr.css('td:nth-child(1)::text').extract_first()
                port = tr.css('td:nth-child(2)::text').extract_first()
                _type = tr.css('td:nth-child(3)::text').extract_first()
                _protocol = tr.css('td:nth-child(4)::text').extract_first()
                _locate = tr.css('td:nth-child(5)::text').extract_first()
                _answer = tr.css('td:nth-child(6)::text').extract_first()
                _time = tr.css('td:nth-child(7)::text').extract_first()
                created_at = int(time.mktime(time.strptime(_time.strip(), '%Y-%m-%d %H:%M:%S')))
                if (curr_time - (3600 * 36) > created_at) :
                    raise Exception('guo qi shu ju, zhi jie wu shi')
		memo = '%s | %s | %s | %s | swei360.com' % (_protocol, _type, _locate, _answer)
                sql += "('%s', %d, 0, '%s', 0, %d)," % (ip, int(port), memo, created_at)

            sql = sql.strip(',')
            item = SpiderSqlItem()
            item['sql'] = sql
            yield item
        except:
            print('analysis tr error')

        try:
            next_url = response.css('#listnav ul a:nth-last-child(5)::attr(href)').extract_first()
            next_page = next_url.split('=')[-1]
            curr_page = response.url.split('=')[-1]
            if int(curr_page) < int(next_page):
                _url = urlparse.urljoin(response.url, next_url)
                yield scrapy.Request(url=_url, callback=self.parse)
            else:
                print('curr page is last, curr url is : ' + response.url)
        except:
            print('next url get error, curr url is : ' + response.url)
        pass




