# __author__ = 'Ricky'
# -*- coding:utf8 -*-

import time
import pandas as pd
import requests
import json
from lxml import etree

headers = {'Host': 'www.duanrong.com',
           'Connection': 'keep-alive',
           'Content-Length': '0',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Origin': 'http://www.duanrong.com',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           }

result = pd.DataFrame()
urls = []
miss_page= []
miss_url = []

for i in range(1, 7):
    try:
        response = requests.get('http://www.duanrong.com/yjtn/list?pageNo=%d' % i, headers=headers)
        if response.status_code == 200:
            tree = etree.HTML(response.text)
            urls = urls + tree.xpath('//*[@id="loanlist"]/div/div/div[2]/div/ul/li/a/@href')
        else:
            miss_page.append(i)
        time.sleep(1.1)
    except Exception, e:
        print i, str(e)
        miss_page.append(i)


for url in urls:
    try:
        response = requests.post('http://www.duanrong.com' + url, headers=headers)
        if response.status_code == 200 and response.json()['status'] == 'SUCCESS':
            slist = pd.DataFrame(response.json()['response']['subjectList'])
            slist[u'随心投'] = url.split('/')[-1]
            result = pd.concat([result, slist])
        else:
            miss_url.append(url)
        time.sleep(1.1)
    except Exception, e:
        print url, str(e)
        miss_url.append(url)

result.to_csv('duanrong_sxt.csv', encoding='gb2312')
            

if __name__ == "__main__":
    pass



