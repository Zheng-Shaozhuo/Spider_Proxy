# -*- coding: utf-8 -*-
import re

import scrapy
import time

from ..items import ProxySqlItem


class BaibianSpider(scrapy.Spider):
    name = 'baibian'
    allowed_domains = ['baibianip.com']
    start_urls = ['https://www.baibianip.com/home/free.html']

    def parse(self, response):
        try:
            sql = 'insert into proxies(ip, port, valid, memo, last_check_timestamp, created_at) values'
            for tr in response.css('.main .action-table table tbody tr'):
                buff = tr.css('td:nth-child(1)').extract_first()
                pos_start = buff.find('</script>') + 9
                pos_end = buff.find('</td>')
                ip = buff[pos_start : pos_end]
                port = tr.css('td:nth-child(2)::text').extract_first()
                _protocol = tr.css('td:nth-child(6)::text').extract_first()
                _type = tr.css('td:nth-child(5)::text').extract_first()
                _contury = tr.css('td:nth-child(3)::text').extract_first()
                _rate = tr.css('td:nth-child(9)::text').extract_first()
                _valide = tr.css('td:nth-child(10)::text').extract_first()
                _last_check = tr.css('td:nth-child(11)::text').extract_first().strip()[0]
                memo = '%s | %s | %s | %s | %s | %s | baibianip.com' % (_protocol, _type,_contury, _rate, _valide, _last_check)
                sql += "('%s', %d, 0, '%s', 0, %d)," % (ip, int(port), memo, int(time.time()) - (int(_last_check) * 60))
            sql = sql.strip(',')
            item = ProxySqlItem()
            item['sql'] = sql
            yield item
        except:
            print('analysis tr error')
        pass

