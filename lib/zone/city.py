#!/usr/bin/env python
# coding=utf-8


import sys
from lib.utility.version import PYTHON_3
from lib.utility.log import *

cities = {

    'bj': '北京',
    'cd': '成都',
    'cq': '重庆',
    'wx': '无锡',
    'gz': '广州',
    'hz': '杭州',
    'hf': '合肥',
    'xa': '西安',
    'nj': '南京',
    'sh': '上海',
    'sz': '深圳',
    'gs': '苏州',
    'tj': '天津',
    'wh': '武汉'
}


lianjia_cities = cities
beike_cities = cities


def create_prompt_text():
    """
    根据已有城市中英文对照表拼接选择提示信息
    :return: 拼接好的字串
    """
    city_info = list()
    count = 0
    for en_name, ch_name in cities.items():
        count += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if count % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city do you want to crawl?\n' + ''.join(city_info)


def get_chinese_city(en):
    """
    拼音拼音名转中文城市名
    :param en: 拼音
    :return: 中文
    """
    return cities.get(en, None)


def get_city():
    city = None
    # 允许用户通过命令直接指定
    if len(sys.argv) < 2:
        print("Wait for your choice.")
        # 让用户选择爬取哪个城市的二手房小区价格数据
        prompt = create_prompt_text()
        # 判断Python版本
        if not PYTHON_3:  # 如果小于Python3
            city = raw_input(prompt)
        else:
            city = input(prompt)
    elif len(sys.argv) == 2:
        city = str(sys.argv[1])
        print("City is: {0}".format(city))
    else:
        print("At most accept one parameter.")
        exit(1)

    chinese_city = get_chinese_city(city)
    if chinese_city is not None:
        message = 'OK, start to crawl ' + get_chinese_city(city)
        print(message)
        logger.info(message)
    else:
        print("No such city, please check your input.")
        exit(1)
    return city


if __name__ == '__main__':
    print(get_chinese_city("sh"))
