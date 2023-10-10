"""
    使用flask本地测试机器人
"""
import sys

sys.path.append("src/lib")
from flask import request, Response
import flask
from telerobot_handler import handle_message_async

app = flask.Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    if request.method != "POST":
        return Response(status=400, response="Bad Request")
    data = request.get_json()
    handle_message_async(data)
    return Response(status=200, response="OK")


@app.route("/upload-image", methods=["POST", "GET"])
def upload_image():
    from apple_shortcut_handler import handler

    return handler({"headers": request.headers, "body": request.get_data()}, None).get('body')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True, use_reloader=False)
