import datetime
from collections import OrderedDict

from motor.motor_tornado import MotorClient

from config import MONGO_URI, MONGO_DB
from utils.about_date import get_last_month

novel_client = MotorClient(MONGO_URI)
novel_db = novel_client[MONGO_DB]


async def motor_weather_save(weather_info, date, type_of=''):
    """爬虫数据保存到mongodb"""
    if not type_of:
        # add_time = time.strftime('%Y-%m-%d %H',time.localtime(time.time()))
        document = {'current_data': weather_info[0], 'max_data': weather_info[1], 'min_data': weather_info[2],
                    'add_time': date,
                    'wind': weather_info[3], 'shidu': weather_info[4],
                    'ziwaixian': {"qiangdu": weather_info[5], "info": weather_info[6]},
                    'ganmao': {
                        "iseasy": weather_info[7],
                        "info": weather_info[8]
                    },
                    "dress": {
                        "wendu": weather_info[9],
                        "info": weather_info[10]
                    },
                    "xiche": {
                        "shifou": weather_info[11],
                        "info": weather_info[12]
                    },
                    "exercise": {
                        "shifou": weather_info[13],
                        "info": weather_info[14]
                    },
                    "kongqiwuran": {
                        "state": weather_info[15],
                        "info": weather_info[16]
                    },
                    "sun_or_not": weather_info[17]}
        result = await novel_db['wx_app_index'].insert_one(document)
    elif type_of == 'xingzuo':
        document = {
            "date": date,
            "total": weather_info[0],
            "love": weather_info[1],
            "career": weather_info[2],
            "money": weather_info[3],
            "heath": weather_info[4],
            "luck_color": weather_info[5],
            "luck_number": weather_info[6],
            "short": weather_info[7]
        }
        result = await novel_db['xingzuo_info'].insert_one(document)
    return result


async def motor_weather_read(date):
    """
        返回天气内容
    :param novel_name:
    :param chapter:
    :return:
    """
    weather_info = await novel_db['wx_app_index'].find_one({'add_time': date})
    if weather_info:
        del weather_info['_id']
    return weather_info


async def motor_find_novel_list(novel_name):
    """
        返回小说列表
    :param novel_name:
    :return:
    """
    novel_list = []
    if not novel_name:
        async for novel in novel_db['novel_info'].find({}).sort([('hot_number', -1)]):  # -1 从大到小
            del novel['_id']
            del novel['description']
            novel_list.append(novel)
        return novel_list
    novel_list = await novel_db['novel_info'].find_one({'name': novel_name})
    del novel_list['_id']
    return novel_list


async def motor_get_last_six_month_bill():
    """
        获取前6个月的账单总额
    :param date:
    :return:
    """
    today = datetime.datetime.now()
    i = 0
    month_list = OrderedDict()
    while i < 6:
        month_list[today.strftime("%m")] = 0
        today = get_last_month(today)
        i += 1
    last_six_month = today.strftime("%Y-%m-%d")
    last_six_list = []
    async for bill in novel_db['app_jizhang_bill'].find({'date': {"$gt": last_six_month, "$lte": datetime.datetime.now().strftime("%Y-%m-%d")}}).sort([('date', 1)]):
        del bill['_id']
        last_six_list.append(bill)
    for i in last_six_list:
        month_list[i['date'][5:7]] += float(i['money'])
    bill_list = list(month_list.values())[::-1]
    month_list = list(month_list.keys())[::-1]
    return month_list, bill_list


async def motor_get_this_month_bill_data(date):
    """
        获取某个月所有的账单信息以及类别
    :param date:
    :return:
    """
    bills_data = []
    async for bill in novel_db['app_jizhang_bill'].find({"date":  {"$regex":date}}).sort([('date',-1)]):
        del bill['_id']
        bills_data.append(bill)
    result = {}
    for i in bills_data:
        result[int(i['father_level'])] = round(result.setdefault(int(i['father_level']), 0) + float(i['money']), 2)
    data_result = list(result.values())
    list_result = list(result.keys())
    return data_result, bills_data, list_result


async def motor_save_bill(data):
    """
        存储账单信息
    :param data:
    :return:
    """
    # date = data['data']['date']
    # money = data['data']['money']
    # father_level = data['data']['father_level']
    # child_level = data['data']['child_level']
    if not data['data']['information']:
        data['data']['information'] = '没有备注信息'
    time = data['time']
    data['data']['add_time'] = time
    result = await novel_db['app_jizhang_bill'].insert_one(data['data'])
    return result


async def motor_get_bill(pages, per_page, reverse):
    """
        获取账单信息
    :return:
    """
    bills = []
    is_reverse = -1
    if reverse == 'false':
        is_reverse = 1
    async for bill in novel_db['app_jizhang_bill'].find({}).sort([('date', is_reverse)]).skip((pages - 1) * per_page).limit(per_page):
        del bill['_id']
        bills.append(bill)
    total = await novel_db['app_jizhang_bill'].count_documents({})
    return bills, total


if __name__ == '__main__':
    pass
