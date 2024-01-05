基于 AWS S3&Lambda&APIGateway 部署的自用图床/小文件分享。
使用Telegram/Apple Shortcut进行交互。

# 步骤

1. 新建S3储存桶

2. 新建可以访问桶的用户，导出密钥文件，内含需要密钥

3. 新建LambdaAPI，将src文件夹内所有文件压缩为zip文件上传、部署

4. 新建APIGateway，将路由设置为新建的LambdaAPI函数

   **注意默认timeout时间为3s，时间太短，建议改为10s以上**

5. 新建telegram 机器人，获得需要的Token

# 配置

```python
# env.py example
# aws key
REGION_NAME="ap-east-1"
AWS_ACCESS_KEY = "<your access key>"
AWS_SECRET_ACCESS_KEY="<your secret access key>"
DEFAULT_BUCKET = "<your bucket>"
DEFAULT_URL = "<bocket url or self domain>"

# telegram robot key
TOKEN = "<your token>"
ALLOWED_USERS = ["user_a", "user_b"] # optional, [] for all users
```

直接修改 telerotot_handler.py 中的get_upload_path来更改保存文件的路径。

# 快捷指令
复用代码来实现一个Apple快捷指令版本的上传功能。需要修改 `lambda_function`中第9行

```python
# from telerobot_handler import handler # 修改前
from apple_shorcut_handlrer import handler # 修改后
```
快捷指令`./resource/upload_latest_file.shortcut`
