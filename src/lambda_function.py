"""
    aws lambda create-function 
    !!注意lambda的超时时间，超时失败cloudwatch没有日志很难发现
"""
import json
import sys

sys.path.append("lib")
from telerobot_handler import handler


def lambda_handler(event, context):
    # TODO implement
    return handler(event, context)
