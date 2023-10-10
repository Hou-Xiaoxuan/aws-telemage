import boto3
import logging
from env import (
    REGION_NAME,
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    DEFAULT_BUCKET,
    DEFAULT_URL,
)

client: boto3.client = boto3.client(
    "s3",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def download(filename):
    with open(filename, "wb") as f:
        client.download_fileobj(DEFAULT_BUCKET, filename, f)


def get_content_type(file_name: str):
    extension_to_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "pdf": "application/pdf",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "ogg": "audio/ogg",
        "mp4": "video/mp4",
        "webm": "video/webm",
        "txt": "text/plain",
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "xml": "application/xml",
    }

    file_extension = file_name.split(".")[-1].lower()
    content_type = extension_to_type.get(file_extension, "application/octet-stream")
    return content_type


def get_presigned_url(filename: str) -> str:
    """获取预签名链接"""
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": DEFAULT_BUCKET, "Key": filename},
        ExpiresIn=1000*60*5,
    )


def upload_file(file_content, filename) -> str:
    logging.info(f"uploading {filename}")
    client.put_object(
        Body=file_content,
        Bucket=DEFAULT_BUCKET,
        Key=filename,
        ContentType=get_content_type(filename),
    )
    return DEFAULT_URL + filename
