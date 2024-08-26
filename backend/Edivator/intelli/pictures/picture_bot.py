import requests
import json

API_KEY = ""
SECRET_KEY = ""


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def generate(text, resolution="512*512", style=None):
    url = "https://aip.baidubce.com/rpc/2.0/wenxin/v1/basic/textToImage?access_token=" + get_access_token()

    data = {
        "text": f"{text}",
        "resolution": f"{resolution}"
    }
    if style:
        data['style'] = style

    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def get_img(taskId):
    url = "https://aip.baidubce.com/rpc/2.0/wenxin/v1/basic/getImg?access_token=" + get_access_token()

    payload = json.dumps({
        "taskId": f"{taskId}"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text




