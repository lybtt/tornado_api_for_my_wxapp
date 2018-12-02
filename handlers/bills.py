import time
import tornado.gen
import json
from handlers.basehandlers import BaseHandler
from dbs.motor_mongo import motor_save_bill, motor_get_this_month_bill_data, motor_get_last_six_month_bill, motor_get_bill


class BillsHandler(BaseHandler):
    """
        账单
        post / get
    """

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        result = yield motor_save_bill(data)
        if result:
            self.set_status(201)
            self.write(json.dumps({'state': 'success'}, ensure_ascii=False))
        else:
            self.write(json.dumps({'state': 'fail'}, ensure_ascii=False))

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 15))
        reverse = self.get_argument('reverse', 'true')
        isthismonth = self.get_argument('this_month', '')
        date = time.strftime('%Y-%m', time.localtime(time.time()))
        date = self.get_argument('date', date)
        is_six = self.get_argument('is_six', '')
        if isthismonth:
            piedata, bills_data, list_result = yield motor_get_this_month_bill_data(date)
            self.set_header('content-type', 'application/json')
            self.finish({"bills_data": bills_data, 'piedata': piedata, 'list_result': list_result})
        elif is_six:   # 返回6个月的数据
            month_list, bill_list = yield motor_get_last_six_month_bill()
            self.set_header('content-type', 'application/json')
            self.finish({"bill_list": bill_list, "month_list": month_list})
        else:
            bills, total = yield motor_get_bill(page, per_page, reverse)
            self.set_header('content-type', 'application/json')
            self.finish({"bills": bills, "total": total})