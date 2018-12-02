import datetime

today = datetime.datetime.now()


def get_last_month(date):
    """
        获取上个月的最后一天
    :param date:
    :return:
    """
    first_day = date.replace(day=1)   # 获取当前月份的第一天
    last_month = first_day - datetime.timedelta(days=1)    # 上个月最后一天
    return last_month

