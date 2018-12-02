import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """解决JS跨域请求问题"""

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/x-www-form-urlencoded;charset=utf-8')
