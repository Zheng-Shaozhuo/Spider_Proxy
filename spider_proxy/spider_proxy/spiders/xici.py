# -*- coding: utf-8 -*-

import urlparse
import scrapy
import time

from ..items import SpiderSqlItem


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1', 'http://www.xicidaili.com/nt/1']
    flag = True

    def parse(self, response):
        try:
	    curr_time = int(time.time())
            sql = 'insert into proxies(ip, port, valid, memo, last_check_timestamp, created_at) values'
            for tr in response.css('#ip_list tr'):
                ip = tr.css('td:nth-child(2)::text').extract_first()
                if ip is None:
                    continue
                port = tr.css('td:nth-child(3)::text').extract_first()
                _protocol = tr.css('td:nth-child(6)::text').extract_first()
                _type = tr.css('td:nth-child(5)::text').extract_first()
                _addr = tr.css('td:nth-child(4) a::text').extract_first()
                _live = tr.css('td:nth-child(9)::text').extract_first()
                _check_time = tr.css('td:nth-child(10)::text').extract_first()
                created_at = int(time.mktime(time.strptime(_check_time.strip(), '%y-%m-%d %H:%M')))
                if (curr_time - (3600 * 36) > created_at) :
		    if (self.flag == False):
			return
		    self.flag = False
                    break 
		memo = '%s | %s | %s | %s | %s | xicidaili.com' % (_protocol, _type, _addr, _live, _check_time)
                sql += "('%s', %d, 0, '%s', 0, %d)," % (ip, int(port), memo, created_at)
            sql = sql.strip(',')
            item = SpiderSqlItem()
            item['sql'] = sql
            yield item
        except:
            print('analysis tr error')

        try:
            next_url = response.css('#body div.pagination a.next_page::attr(href)').extract_first()
            if next_url is not None:
                _url = urlparse.urljoin(response.url, next_url)
                yield scrapy.Request(url=_url, callback=self.parse)
            else:
                print('curr page is last, curr url is : ' + response.url)
        except:
            print('next url get error, curr url is : ' + response.url)
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        pass
