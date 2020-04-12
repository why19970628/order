"""不使用原有的资源目录，改变路径，解决无法加载的问题"""
from flask import Blueprint, send_from_directory
from application import app

route_static = Blueprint('static', __name__)


@route_static.route('/<path:filename>')
def index(filename):
    app.logger.info(filename)
    return send_from_directory(app.root_path + '/web/static', filename)
