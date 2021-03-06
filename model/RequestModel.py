#!/usr/bin/env python
# coding=utf-8
import json
import os
import random

import requests

import cfg
import model.my_proxy as my_proxy


class RequestModel(object):
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"
    ]

    # 代理池，两种类型
    Proxy_Pool_http = []
    Proxy_Pool_https = []
    no_proxy = {}

    def __init__(self):
        """
        初始化的目的：将json文件转移到proxy_poll_http等两个私有变量中
        """
        dataPath = os.path.abspath(cfg.RootPath + '\\model\\proxy_ip.json')  # 获取tran.csv文件的路径
        with open(dataPath, 'r', encoding='utf8') as f:
            # dict_ip = json.load(f)
            content = f.readlines()
            for line in content:
                data = json.loads(line)
                data_type = data['type']
                result = str(data['host']) + ':' + str(data['port'])
                # 根据http类型，加入到相应的列表中
                if data_type == 'http':
                    self.Proxy_Pool_http.append(result)
                elif data_type == 'https':
                    self.Proxy_Pool_https.append(result)
                else:
                    continue

    # 获取不同的请求头
    def get_headers(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache - Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.dy1234.net',
            'DNT': '1',
            'Pragma': 'no-cache',
            # 'Referer': 'http: //www.dytt8.net/html/gndy/dyzz/index.html',
            'Cookie': 'UM_distinctid=174c60df6f4807-070d6885205e05-7e647b65-1fa400-174c60df6f5955; CNZZDATA1276470129=299915948-1601046745-%7C1606627666; '
                      'Hm_lvt_b12979e4e40bb5a6bba9824601810548=1606542703,1606561256,1606625698,1606631576; ASPSESSIONIDSQAARADT=MHHHEIMDLCDMDBPCELHDFMGC',
            'User-Agent': random.choice(self.UserAgent_List),
        }
        return headers

    # 验证、获取代理
    def get_proxies(self):
        pre_data = random.choice(self.Proxy_Pool_http)
        ip, port = pre_data.split(':')
        proxies = {}
        # 如果当前代理通过的话
        if my_proxy.test_proxy(ip, port, 'http'):
            proxies = {
                'http': pre_data
                # 'http':'web-proxy.oa.com:8080',
                # 'https': random.choice(cls.Proxy_Pool)
            }
            print('当前所使用的代理为:' + str(proxies))
        else:
            self.get_proxies()  # 简单的递归，直至选出有效的代理。但当代理全部无效的时候，将陷入死循环
        return proxies

    # 返回一个request连接
    def new_request(self, url):
        requests.adapters.DEFAULT_RETRIES = 20  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        # proxies=self.get_proxy 为使用代理；no_proxy 不使用代理
        return s.get(url, headers=self.get_headers(), proxies=self.no_proxy, timeout=cfg.TIMEOUT + 1000)


if __name__ == '__main__':
    temp = RequestModel()
    # temp.get_proxies()
    response = temp.new_request(cfg.WEBSITE + 'w.asp?p=1&f=3&l=t')
    print(response)
