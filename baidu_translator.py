# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/8

import requests
import json

# 百度AI平台的AppID、API Key、Secret Key
APP_ID = '115789030'
API_KEY = 'vI7EoNKX40pDiXmcST1IGkVZ'
SECRET_KEY = '73GwXFVKOOOOhKwoCFxSEa3t2fx0zUnr'


def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vI7EoNKX40pDiXmcST1IGkVZ&client_secret=73GwXFVKOOOOhKwoCFxSEa3t2fx0zUnr"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return response.json()['access_token']


token = get_token()
url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=' + token

def baidu_trans(q):
    # For list of language codes, please refer to `https://ai.baidu.com/ai-doc/MT/4kqryjku9#语种列表`
    from_lang = 'en' # example: en
    to_lang = 'zh' # example: zh
    term_ids = '' # 术语库id，多个逗号隔开

    # Build request
    headers = {'Content-Type': 'application/json'}
    payload = {'q': q, 'from': from_lang, 'to': to_lang, 'termIds' : term_ids}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    result_str = json.dumps(result, indent=4, ensure_ascii=False)
    print(result_str)
    result_text = result["result"]["trans_result"][0]["dst"]
    print(f"result_text: {result_text}")
    return result_text


# baidu_trans('Hello, how are you?')



# {
#     "result": {
#         "from": "en",
#         "trans_result": [
#             {
#                 "dst": "你好吗？",
#                 "src": "Hello, how are you?"
#             }
#         ],
#         "to": "zh"
#     },
#     "log_id": 1843618188583680230
# }

