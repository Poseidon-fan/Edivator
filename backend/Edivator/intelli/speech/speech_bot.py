import base64
import urllib
import requests
import json

from intelli.speech.test import base64_speech

API_KEY = "XswLNPbjROFUPr658lbiq6k0"
SECRET_KEY = "XjWqm5MjWn2KgoyjI0xKqUloHy0QnLTo"


def recognize(file_format, user_id, speech, dev_pid=1537):
    url = "https://vop.baidu.com/server_api"
    payload = json.dumps({
        "format": file_format,
        "rate": 16000,
        "channel": 1,
        "cuid": f"{user_id}",
        "token": get_access_token(),
        "speech": speech,
        "len": len(base64.b64decode(speech)),
        "dev_pid": dev_pid
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
