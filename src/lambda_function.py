"""
    aws lambda create-function 
    !!注意lambda的超时时间，超时失败cloudwatch没有日志很难发现
"""
import json
import sys

sys.path.append("src/lib")
from robot import handle_message
import awsclient

def lambda_handler(event, context):
    # TODO implement
    body = event["body"]
    data = json.loads(body)
    handle_message(data)  # lambda函数不支持异步
    return {"statusCode": 200}
