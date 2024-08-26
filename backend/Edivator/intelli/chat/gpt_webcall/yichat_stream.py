from pprint import pprint
import requests
import json
from _token_manager import get_access_token


def yichat_stream(content: str):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "assistant",
                "content": content
            }
        ],
        "stream": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, stream=True)

    for line in response.iter_lines():
        if line:
            yield line.decode("UTF-8")
