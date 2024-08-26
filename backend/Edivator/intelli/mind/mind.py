import requests
import json

API_KEY = "XAfWvj0k0MfTww8Lk89BSVOB"
SECRET_KEY = "YHEr1UI1SVD9Uo6ohoRo56kdlrEcGgkA"

import re

def generate_node_array(markdown_text):
    # 正则表达式匹配 Markdown 标题
    title_pattern = re.compile(r'^(#+)\s+(.*)')
    lines = markdown_text.split('\n')
    
    # 用于存储结果的列表
    result = []
    
    # 用于存储当前层级的父id
    parent_ids = {0: None}
    current_level = 0
    
    for line in lines:
        match = title_pattern.match(line)
        if match:
            hashes, title = match.groups()
            level = len(hashes)  # 标题层级
            
            # 更新parent_ids字典
            if level > current_level:
                parent_ids[level] = title
            elif level < current_level:
                for i in range(current_level, level, -1):
                    del parent_ids[i]

            current_level = level
            parent_id = parent_ids.get(level - 1, None)
            
            # 创建节点字典
            node = {
                'id': title,
                'topic': title
            }
            if level == 1:
                node['isroot'] = True
            else:
                node['parentid'] = parent_id
            
            result.append(node)
    
    return result


def gen_mind(content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                'role': "user",
                'content': f'我要写一篇文章，标题为“{content}”，请给我推荐一个文章结构，即各级标题（每行都以若干#开头），用markdown语法输出。只要输出markdown内容，不要输出任何其他内容'
            }
        ],
        "temperature": 0.95,
        "top_p": 0.8,
        "penalty_score": 1,
        "disable_search": False,
        "enable_citation": False,
        "response_format": "text"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    markdown = response.json()['result']
    return generate_node_array(markdown)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

