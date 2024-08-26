import pprint
import requests
import json
from _token_manager import get_access_token


def yichat_single_round(content: str):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("result")


if __name__ == '__main__':
    response = yichat_single_round("你可以文生图吗？")
    pprint.pprint(response)
