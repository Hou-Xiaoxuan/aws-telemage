"""
    使用flask测试机器人
"""
import sys
sys.path.append("src/lib")
from flask import request, Response
import flask
from robot import handle_message_async

app = flask.Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    if request.method != "POST":
        return Response(status=200, response="OK")
    data = request.get_json()
    handle_message_async(data)
    return Response(status=200, response="OK")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
