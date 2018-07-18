import json

import pymysql
import requests
import threadpool
import time

_list = []
def _check(protocol, proxy, _id):
    url = 'http://ip.chinaz.com/getip.aspx'
    # https_url = 'https://www.zhihu.com/people/mokaprince'
    proxies = {}
    proxies[protocol] = proxy
    try:
        response = requests.get(url=url, proxies=proxies, timeout=5)
        # response = requests.get(url=https_url, proxies=proxies, timeout=5)
        if '{ip' in response.text:
            _update('valid = 1' + ', last_check_timestamp = ' + str(int(time.time())), 'id = ' + str(_id))
        else:
            _update('valid = 0' + ', last_check_timestamp = ' + str(int(time.time())), 'id = ' + str(_id))
    except:
        _update('valid = 0' + ', last_check_timestamp = ' + str(int(time.time())), 'id = ' + str(_id))
        print proxy + ' connect failed\n'
    else:
        print proxy + ' success\n'

def get_proxy_list_by_mysqldb(sql):
    conn = pymysql.connect(host='*.*.*.*', port=3306, user='***', passwd='*********', db='vv_spider', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows

def _update(where, set):
    sql = 'update proxies set %s where %s' % (where, set)
    conn = pymysql.connect(host='*.*.*.*', port=3306, user='***', passwd='*********', db='vv_spider', charset='utf8')
    cursor = conn.cursor()
    effect_row = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def dispatch_row(_str):
    params = str(_str).split('=')
    check_proxies_valid(str(params[1]).split(':')[0], params[1], params[0])

sql = "select id, ip, port from proxies"
rows = get_proxy_list_by_mysqldb(sql)

for row in rows:
    _list.append(('%d=http://%s:%d' % (row[0], row[1], row[2])))


pool = threadpool.ThreadPool(32)
_requests = threadpool.makeRequests(dispatch_row, _list)
[pool.putRequest(req) for req in _requests]
pool.wait()
