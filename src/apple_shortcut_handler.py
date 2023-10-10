from awsclient import upload_file


def handler(event: dict, context: dict) -> dict:
    """处理lambda请求，并返回链接"""
    headers = event["headers"]
    if "image" not in headers.get("content-type"):
        return {"statusCode": 400, "body": "content-type must be image/jpeg"}
    try:
        filename = headers["filename"]
        fileext = headers["fileext"]
        filecontent = event["data"]
    except Exception as e:
        return {"statusCode": 400, "body": f"parse body error: {str(e)}"}
    # {year}/{month}/{year}{month}{day}-{random}-{filename}{.suffix}
    import datetime
    import random

    now = datetime.datetime.now()
    try:
        path = f"{now.year}/{now.month}/{now.year}-{now.month}-{now.day}-{random.randint(1000, 9999)}-{filename}.{fileext}"
        url = upload_file(file_content=filecontent, filename=path)
    except Exception as e:
        return {"statusCode": 400, "body": f"upload failed: {str(e)}"}
    return {"statusCode": 200, "message": "ok", "body": url}
