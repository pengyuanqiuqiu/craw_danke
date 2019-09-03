#!/usr/bin/env python
# coding=utf-8

import requests
from lxml import etree
from lib.request.headers import *

chinese_city_district_dict = dict()     # 城市代码和中文名映射
chinese_area_dict = dict()              # 版块代码和中文名映射
area_dict = dict()


def get_chinese_district(en):
    """
    拼音区县名转中文区县名
    :param en: 英文
    :return: 中文
    """
    return chinese_city_district_dict.get(en, None)


def get_districts(city):
    """
    获取各城市的区县中英文对照信息
    :param city: 城市
    :return: 英文区县名列表
    """
    url = 'http://www.danke.com/room/{0}/'.format(city)
    headers = create_headers()
    response = requests.get(url, timeout=10, headers=headers)
    html = response.content
    root = etree.HTML(html)
    elements = root.xpath('/html/body/div[3]/div/div[4]/div[2]/dl[2]/dd/div/div/a')
    dis_names = list()
    result =list()
    number = 1
    for element in elements:
        dis_names.append(element.text.strip())
        elemen=root.xpath('/html/body/div[3]/div/div[4]/div[2]/dl[2]/dd/div/div[%s]/div/a' % number)
        area_names = list()
        for ele in elemen:
            area_names.append(ele.text.strip())
        number +=1
        result.append({"districts":element.text.strip(),"area":area_names})
    return dis_names,result

if __name__ == '__main__':
    get_districts('sz')