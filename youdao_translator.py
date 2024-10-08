# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/9

import requests
from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '0de3dc1d6ceb1402'
# 您的应用密钥
APP_SECRET = 'ARfGK2QZsPWAVc7zfmmSg9h1ZhR2tWri'


def youda_trans(q):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    # q = 'there is a white cat sitting on a table with a christmas tree in the background' # 'there is a white cat sitting on a table with presents'
    lang_from = 'en'
    lang_to = 'zh-CHS'
    # vocab_id = ''

    data = {'q': q, 'from': lang_from, 'to': lang_to} # , 'vocabId': vocab_id

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    # print(type(res.json()))
    res_json = res.json()
    print(res_json["query"])
    print(res_json["translation"][0])
    return res_json["translation"][0]



def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


# youda_trans("there is a white cat walking in a living room with a bed")