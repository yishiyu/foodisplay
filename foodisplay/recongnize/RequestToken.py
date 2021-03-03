#!  conda env
# -*- coding:utf-8 -*-
# Time:2021/2/23 下午3:57
# Author : nishizzma
# File : RequestToken.py
"""
获取百度API接口的Token令牌
"""

import requests
from foodisplay import config

# client_id 为官网获取的AK， client_secret 为官网获取的SK
AK = config["WORDAPI"]["AK"]
SK = config["WORDAPI"]["SK"]
HOSTFORMAT = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'
host = HOSTFORMAT.format(AK,SK)
response = requests.get(host)
if response:
    print(response.json())
