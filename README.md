完全基于 AWS 部署的自用 telegram 图床机器人。

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
