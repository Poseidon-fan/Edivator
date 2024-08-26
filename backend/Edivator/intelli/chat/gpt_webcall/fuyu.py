from pprint import pprint
import requests
import json
from Edivator.intelli.gpt_web._token_manager import get_access_token


def main():

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/image2text/fuyu_8b?access_token=" + get_access_token()
    payload = json.dumps({
        "prompt": "introduce the picture",
        "image": "9j/4AAQSkZJRgABAQAAAQABAAD/xxxxx"    # base64 encoded image
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    pprint(response.text)


if __name__ == '__main__':
    main()
