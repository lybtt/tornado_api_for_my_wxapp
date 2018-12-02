import tornado.gen

from .basehandlers import BaseHandler
from dbs.motor_mongo import motor_find_novel_list


class NovelListHandler(BaseHandler):
    """
        小说列表
    """
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        novel_name = self.get_argument('novel_name', '')
        result = yield motor_find_novel_list(novel_name)
        self.set_header('content-type', 'application/json')
        self.finish({"novel_list": result})