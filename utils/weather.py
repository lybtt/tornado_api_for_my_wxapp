from lxml import etree

url = 'http://forecast.weather.com.cn/town/weather1dn/101020600014.shtml'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/68.0.3423.2 Safari/537.36"

headers = {"User-Agent": USER_AGENT}


def parse_html(content):
    html = etree.HTML(content)

    # 当前温度
    data = html.xpath('/html/body/div[4]/div[3]/div[2]/div[3]/span[1]')
    data = data[0].text + '℃'
    # print(data)

    # 阴晴
    sun_or_not = html.xpath('/html/body/div[4]/div[3]/div[2]/div[4]')
    sun_or_not = sun_or_not[0].text
    # print(sun_or_not)

    # 最大温度
    maxTempDiv = html.xpath('//*[@id="maxTempDiv"]/span')
    maxTempDiv = maxTempDiv[0].text
    # print(maxTempDiv)

    # 最低温度
    minTempDiv = html.xpath('//*[@id="minTempDiv"]/span')
    minTempDiv = minTempDiv[0].text
    # print(minTempDiv)

    # 风向
    wind = html.xpath('/html/body/div[4]/div[3]/div[2]/p[1]/span')
    wind = wind[0].text
    # print(wind)

    # 湿度
    shidu = html.xpath('/html/body/div[4]/div[3]/div[2]/p[2]/span')
    shidu = shidu[0].text
    # print(shidu)

    # 紫外线
    ziwaixian = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[1]/dt/em')
    ziwaixian = ziwaixian[0].text
    # print(ziwaixian)

    # 紫外线提示
    ziwaixian_info = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[1]/dd')
    ziwaixian_info = ziwaixian_info[0].text
    # print(ziwaixian_info)

    # 感冒
    ganmao = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[2]/dt/em')
    ganmao = ganmao[0].text
    # print(ganmao)

    # 感冒信息
    ganmao_info = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[2]/dd')
    ganmao_info = ganmao_info[0].text
    # print(ganmao_info)

    # 穿衣
    chuanyi = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[3]/dt/em')
    chuanyi = chuanyi[0].text
    # print(chuanyi)

    # 穿衣信息
    chuanyi_info = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[3]/dd')
    chuanyi_info = chuanyi_info[0].text
    # print(chuanyi_info)

    # 洗车
    xiche = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[4]/dt/em')
    xiche = xiche[0].text
    # print(xiche)

    # 洗车信息
    xiche_info = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[4]/dd')
    xiche_info = xiche_info[0].text
    # print(xiche_info)

    # 运动
    yundong = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[5]/dt/em')
    yundong = yundong[0].text
    # print(yundong)

    # 运动信息
    yundong_info = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[5]/dd')
    yundong_info = yundong_info[0].text
    # print(yundong_info)

    # 空气污染
    kongqiwuran = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[6]/dt/em')
    kongqiwuran = kongqiwuran[0].text
    # print(kongqiwuran)

    # 空气污染信息
    kongqiwuran_info = html.xpath('/html/body/div[4]/div[4]/div[1]/div/dl[6]/dd')
    kongqiwuran_info = kongqiwuran_info[0].text
    # print(kongqiwuran_info)
    del content
    return [data, maxTempDiv, minTempDiv, wind, shidu, ziwaixian, ziwaixian_info, ganmao, ganmao_info, chuanyi, \
            chuanyi_info, xiche, xiche_info, yundong, yundong_info, kongqiwuran, kongqiwuran_info, sun_or_not]
