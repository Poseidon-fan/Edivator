import requests
import json
from _token_manager import get_access_token


def main():

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "hi"
            },
            {
                "role": "assistant",
                "content": "Hello! How can I assist you today? If you have any questions or need information on a specific topic, feel free to ask."
            },
            {
                "role": "user",
                "content": "Please introduce The Great Wall"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()
