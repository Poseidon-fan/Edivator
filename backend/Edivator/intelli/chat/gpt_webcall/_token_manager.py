from pprint import pprint
import requests
import json

def get_tokens():
    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=jMi5FcOK8w0EaTMOMhY8sA2H&client_secret=CEep2PHZPSgep9sH4ayzzDfHnrLYCQpz&grant_type=client_credentials"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_access_token():
    return get_tokens().get("access_token")


if __name__ == '__main__':
    # token = get_access_token()
    token = get_tokens()
    pprint(token)
