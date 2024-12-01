import requests

# 定义请求的URL
url = "http://127.0.0.1:8000/KG_Talk"

# 构建请求数据
data = {
    "query": "介绍下白石",  # 替换为实际查询内容
    "type": "global"#local
}

"""
    GLOBAL = "global"
    LOCAL = "local"#节点描述做召回 找小节点->小节点边->再找社区
"""

# 发送POST请求
response = requests.post(url, json=data)



# 检查响应状态码
if response.status_code == 200:
    # 打印响应结果
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)