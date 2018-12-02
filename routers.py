from handlers.weather import WeatherHandler
from handlers.novel_list import NovelListHandler
from handlers.bills import BillsHandler

HANDLERS = [
    (r"/api/weather", WeatherHandler),
    (r"/api/novel", NovelListHandler),
    (r"/api/bills", BillsHandler),
]
