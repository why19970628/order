SERVER_PORT = 9000
DEBUG = False
SQLALCHEMY_ECHO = False  # 打印sql语句
AUTH_COOKIE_NAME = 'mooc_food'

# 过滤url
IGNORE_URLS = [
    '^/user/login',
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]
API_IGNORE_URLS = [
    '^/api'
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    '1': '正常',
    '0': '已删除'
}

MINA_APP = {
    'appid': 'wx4f75798909e3e4af',
    'appkey': 'f24a51bf8a8cf49dfb263691bb5db829'
}

UPLOAD = {
    'ext':['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url':'/static/upload/'
}

APP = {
    'domain':'http://127.0.0.1:9000'
}

