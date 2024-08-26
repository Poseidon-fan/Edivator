import requests
import json

API_KEY = "xASkIgrD30xmfUjd7uj7VXzq"
SECRET_KEY = "ibeWsbuK1RF2WpS5Wxm89ZH4gSVIqo9h"


def get_keywords(content, title):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword?charset=UTF-8&access_token=" + get_access_token()

    payload = json.dumps({
        "content": content,
        "title": title
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

