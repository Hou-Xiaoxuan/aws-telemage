基于 AWS S3&Lambda&APIGateway 部署的自用图床/小文件分享。
使用Telegram/Apple Shortcut进行交互。

# 步骤

1. 新建S3储存桶

2. 新建可以访问桶的用户，导出密钥文件，内含需要密钥

3. 新建LambdaAPI，按照需求将对应zip文件上传、部署。zip自动打包方法见下方。

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

效果如图

<img width="364" alt="image" src="https://github.com/Hou-Xiaoxuan/aws-telemage/assets/59465493/e82f9897-6b04-45bf-af30-22fca4937407">


# 快捷指令
复用代码来实现一个Apple快捷指令版本的上传功能。需要修改 `lambda_function`中第9行

```python
# from telerobot_handler import handler # 修改前
from apple_shorcut_handlrer import handler # 修改后
```
快捷指令位于`./resource/upload_latest_file.shortcut`，注意使用需要使用“快捷指令”App编辑替换部署服务的url，当前只支持图片。

<img width="619" alt="image" src="https://github.com/Hou-Xiaoxuan/aws-telemage/assets/59465493/83dbc0ba-69ef-44ab-a975-e778932f808c">

效果如图，成功上传自动复制链接到剪切板。

<img width="661" alt="image" src="https://github.com/Hou-Xiaoxuan/aws-telemage/assets/59465493/005a1060-68a6-48cb-8a4a-f0a1bf15b5a7">


# lambda 代码自动打包
## Lambda 运行环境

- Runtime：Python 3.14
- Handler：`lambda_function.lambda_handler`
- Region：`ap-east-1`
- Telegram 和 Apple Shortcut 使用不同的部署包
- 部署包由 `scripts/build_lambda.sh` 生成
- `src/env.py` 包含敏感配置，请勿上传到公共仓库。

## 构建部署包

本机需要安装 Python 3.14、`pip`、`zip` 和 `unzip`。先从配置模板创建本地配置：

```bash
cp src/env.example.py src/env.py
```

填写 `src/env.py` 后运行：

```bash
./scripts/build_lambda.sh
```

生成以下文件：

```text
dist/telemage-telegram-python314.zip
dist/telemage-shortcut-python314.zip
```

两个 AWS Lambda 均保持 Handler 为 `lambda_function.lambda_handler`，分别上传对应 ZIP，Runtime 设置为 Python 3.14。
