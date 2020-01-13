#!/usr/bin/python3
# -*- coding:utf-8 -*-


import requests
import re
from bs4 import BeautifulSoup
from hashlib import sha1
import time
import random
import json
import logging
from requests.adapters import HTTPAdapter
#from lessonObj import Lesson

session = requests.Session()
UAs = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
]
headers = {
    "User-Agent": UAs[1],  # UAs[random.randint(0, len(UAs) - 1)],  # random UA
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    # "Cookie":"GSESSIONID=F6052EDFBEF1E44EEE69375BA5F233CD;SERVERNAME=s2;JSESSIONID=F6052EDFBEF1E44EEE69375BA5F233CD;semester.id=62"
}

# 设置session的请求头信息
session.headers = headers
host = r'http://218.65.61.79:8002'
requests.adapters.DEFAULT_RETRIES = 5


def simulate_login(stuID, stuPwd, retry_cnt=1):
    """
    登录新教务系统
    :param stuID: 学号
    :param stuPwd: 密码
    :param retry_cnt: 登录重试次数
    :return: name: {str} 姓名(学号)
    """
    try_cnt = 1
    while try_cnt <= retry_cnt:
        session.cookies.clear()  # 先清一下cookie
        r1 = session.get(host + '/eams/login.action', headers={'Connection':'close'})
        # logging.debug(r1.text)

        temp_token_match = re.compile(r"CryptoJS\.SHA1\(\'([0-9a-zA-Z\-]*)\'")
        # 搜索密钥
        if temp_token_match.search(r1.text):
            # print("Search token OK!")
            temp_token = temp_token_match.search(r1.text).group(1)
            logging.debug(temp_token)
            postPwd = temp_token + stuPwd
            # logging.debug(postPwd)

            # 开始进行SHA1加密
            s1 = sha1()  # 创建sha1对象
            s1.update(postPwd.encode())  # 对s1进行更新
            postPwd = s1.hexdigest()  # 加密处理
            try_cnt += 1
            # logging.debug(postPwd)  # 结果是40位字符串

            # 开始登录
            postData = {'username': stuID, 'password': postPwd}
            time.sleep(0.5* try_cnt)  # fix Issue#2 `Too Quick Click` bug, sleep for longer time for a new trial
            r2 = session.post(host + '/eams/login.action', data=postData, headers={'Connection':'close'})
            if r2.status_code == 200 or r2.status_code == 302:
                logging.debug(r2.text)
                temp_key = temp_token_match.search(r2.text)
                if temp_key:  # 找到密钥说明没有登录成功，需要重试

                    temp_key = temp_key.group(1)
                    logging.debug(temp_key)
                    name = None
                    return name
                elif re.search(r"ui-state-error", r2.text):  # 过快点击

                    time.sleep(2)

                    # session.headers["User-Agent"] = UAs[1]  # random.randint(0, len(UAs)-1)  # 换UA也不行
                    # exit(3)
                else:
                    temp_soup = BeautifulSoup(r2.text.encode('utf-8'), 'html.parser')
                    name = temp_soup.find('a', target='_blank').string.strip()
                    #print("{}".format(name))

                    return name

            else:
                # print("Login ERROR!\n")
                exit(1)
        else:
            # print('Search token ERROR!\n')
            exit(1)

    exit(3)








if __name__ == "__main__":
    simulate_login("","")