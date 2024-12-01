
import requests

# 定义请求的URL
url = "http://127.0.0.1:8000/KG_Story"

# 发送POST请求
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    # 打印响应结果
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
