# -*- coding:utf-8 -*-

"""
Created on 2018年07月18日
@author: lowin
@contact: li783170560@126.com

用requests包爬取网站内容，在链接失败后可重复爬取
"""

import requests
import time
def requests_link(url,encoding='utf-8'):
    """
            爬取网站内容，如网站链接失败，可重复爬取20次
            Parameters
            ------
                url: 网站 string
                encoding: 编码类型 string：’utf-8‘、’gbk‘等
            Return
            -------
                r： 爬取返回内容 response: 

        """
    i=0
    while True:
        try:
            r = requests.get(url,timeout = 5)
            r.encoding = encoding
            return r
        except:
            i+=1
            print('第%s次链接失败' %str(i))
            time.sleep(5)
            if i>20:
                return None
