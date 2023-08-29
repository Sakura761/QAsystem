from flask import request,Flask
import flask
from flask_cors import *
from utils import *
from gevent import pywsgi
# 创建视图应用
app = flask.Flask(__name__)
# 解决跨域
CORS(app, supports_credentials=True,resources='/*')
# 编写视图函数，绑定路由
@app.route("/query", methods=["GET"])  # 查询（全部）
def query():
    data = {'success':False}
    question = request.args["question"]
    answer = robot_response(question)
    data['data'] = answer
    data['success'] = True
    return flask.jsonify(data)
# 运行flask：默认是5000端口，此处设置端口为8888
if __name__ == '__main__':
    server = pywsgi.WSGIServer(("0.0.0.0",8888), app)
    server.serve_forever()
