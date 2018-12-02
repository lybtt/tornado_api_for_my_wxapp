import time

import tornado.gen
import tornado.httpclient

import logging

from .basehandlers import BaseHandler

from dbs.motor_mongo import motor_weather_read, motor_weather_save
from utils.weather import parse_html, url

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class WeatherHandler(BaseHandler):
    """
        微信小程序首页，返回天气数据
    """

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        logger = logging.getLogger('weather INFO')
        date = time.strftime('%Y-%m-%d %H', time.localtime(time.time()))
        self.date = self.get_argument('date', date)
        weather_info = yield motor_weather_read(self.date)
        if weather_info:
            logger.info("have data, return data")
        else:
            logger.info("no data, crawl first")
            http = tornado.httpclient.AsyncHTTPClient()
            response = yield http.fetch(url)
            result = yield motor_weather_save(parse_html(response.body), self.date)
            if result:
                weather_info = yield motor_weather_read(self.date)
            else:
                weather_info = 'fail'
        self.set_header('content-type', 'application/json')
        self.finish({"weather_info": weather_info})
