import requests
import datetime
from awsclient import upload_file
from env import ALLOWED_USERS, TOKEN
import logging
import hashlib


def reply_msg(chat_id: int, text: str, message_id=None):
    text.replace(TOKEN, "<ROVOT_TOKEN>")  # 防止暴露敏感信息
    url = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)
    data = {"chat_id": chat_id, "text": text, "reply_to_message_id": message_id}
    try:
        requests.post(url, data=data)
    except Exception as e:
        logging.error(f"reply message error: {str(e)}")


def get_file(file_id: dict) -> bytes:
    """download file from telegram server"""
    url = "https://api.telegram.org/bot{}/getFile".format(TOKEN)
    data = {"file_id": file_id}
    r = requests.post(url, data=data)
    file_path = r.json()["result"]["file_path"]
    url = "https://api.telegram.org/file/bot{}/{}".format(TOKEN, file_path)
    r = requests.get(url)
    return r.content


class TeleFile:
    filename: str
    file_content: bytes
    file_size: int  # MB
    file_type: str

    def __init__(self, filename, file_size, file_type):
        self.filename = filename
        self.file_size = file_size
        self.file_type = file_type


def get_upload_path(file: TeleFile, username: str, message_id: str):
    """生成上传路径
    路径规则：图片放入telemage，文件放入tempfile，按照用户id分文件夹
    文件名：yyyy-mm-dd-message_id-文件名
    """
    user_id = hashlib.sha256(username.encode()).hexdigest()[:16]
    path = "telemage" if file.file_type == "photo" else "tempfile"
    path = (
        "telemage"
        if file.filename.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif"]
        else "tempfile"
    )
    time = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{time}-{message_id}-{file.filename}"
    return f"{path}/{user_id}/{filename}"


def handle_message(data) -> None:
    try:
        chat_id = data["message"]["chat"]["id"]
        message_id = data["message"]["message_id"]
        username = data["message"]["from"]["username"]
    except Exception as e:
        logging.error(f"parse message error: {str(e)}")
        return None

    def _handle_message() -> str:
        """None|str error message"""
        if username not in ALLOWED_USERS:
            return f"Permission denied for user {username}"

        logging.info(f"accept message from: {username}")
        file_type, file_field = None, None
        for key in ["photo", "document", "video", "audio"]:
            if key in data["message"]:
                file_type = key
                file_field = data["message"][key]
                if key == "photo":
                    file_field = file_field[-1]
                    file_field["file_name"] = "compressed_photo.jpg"
                break
        if not file_type:
            return "unsupported file type"

        file = TeleFile(
            filename=file_field["file_name"],
            file_size=file_field["file_size"] / 1024 / 1024,
            file_type=file_type,
        )
        if file.file_size > 200:
            return "file size must less than 200MB"
        try:
            file.file_content = get_file(file_field["file_id"])
        except Exception as e:
            return f"get file error: {str(e)}"

        try:
            upload_file_name = get_upload_path(file, username, message_id)
            url = upload_file(
                filename=upload_file_name,
                file_content=file.file_content,
            )
        except Exception as e:
            return f"upload file error: {str(e)}"

        reply_msg(chat_id, url, message_id)
        return None

    reply_msg(chat_id, "正在处理，请稍后...", message_id)
    err = _handle_message()
    if err:
        reply_msg(chat_id, err, message_id)
        logging.error(f"handle message error: {err}")
    return None


# 异步处理消息
import threading


def handle_message_async(data):
    threading.Thread(target=handle_message, args=(data,)).start()
    return None
