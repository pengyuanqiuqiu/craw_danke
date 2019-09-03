#!/usr/bin/env python
# coding=utf-8
import re
import datetime
import threadpool
from bs4 import BeautifulSoup
from lib.item.zufang import *
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.databese import helper
from lib.utility.path import *
from lib.zone.area import *
from lib.zone.city import get_city
import lib.utility.version
def get_area_zufang_info(city_name, districts, area_name):
    matches = None
    """
    通过爬取页面获取城市指定版块的租房信息
    :param city_name: 城市
    :param area_name: 版块
    :return: 出租房信息列表
    """
    page = 'http://www.danke.com/room/{0}/d{1}-b{2}.html'.format(city_name, districts, area_name)
    headers = create_headers()
    response = requests.get(page, timeout=10, headers=headers)
    html = response.content
    root = etree.HTML(html)
    elements = root.xpath('//div[@class="page"]/a/text()')
    try:
        total_page = len(elements)-1
    except:
        total_page = 0
    headers = create_headers()
    res = []
    page_number =1
    while True:
        page = 'http://www.danke.com/room/{0}/d{1}-b{2}.html?page={3}'.format(city_name, districts, area_name, page_number)
        BaseSpider.random_delay()
        response = requests.get(page, timeout=10, headers=headers)
        page_number += 1
        html = response.content
        page_text =response.text
        if '您查找的房源已售罄' not  in page_text:
            root = etree.HTML(html)
            net_url = root.xpath('//div[@class="r_lbx_cena"]/a/@href')
            title = root.xpath('//div[@class="r_lbx_cena"]/a/@title')
            square =root.xpath('//div[@class="r_lbx_cenb"]/text()')
            square_result =[]
            for i in  square:
                square_result.append(i.replace(" ", "").replace("\t", "").replace("\n", ""))
            square_result =[i for i in square_result if i !=""]
            price = root.xpath('//span[@class="ty_b"]/text()')
            price =[i.replace(" ", "").replace("\t", "").replace("\n", "") for i in price]
            picture = root.xpath('//div[@class="r_lbx"]/a/img/@src')
            for i in range(len(net_url)):
                # res.append([net_url[i], title[i], square_result[i], price[i], picture[i]])
                sql = "insert into xiaoqu (city,date,district,area,xiaoqu,price,picture_url,decribtion)" \
                      " VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(city_name,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                          districts, area_name,title[i],price[i],
                                                         picture[i],square_result[i] )
                helper.insert(sql)
                save_picture(picture[i],title[i],city_name, districts, area_name)
        else:
            break
def save_picture(url,title_name,city_name, districts, area_name):
    if url[0:2]=='//':
        url='http:'+url
    img = requests.get(url)
    picture = create_picture_path(city_name, districts, area_name)
    picture_url =picture+title_name.replace(" ", "")+ ".jpg"
    if os.path.exists(picture_url):
        picture_url=picture+title_name.replace(" ", "")+ str( random.randint(0,20000))+ ".jpg"
    try:
        open(picture_url, 'wb').write(img.content)
        return picture_url
    except Exception as e:
        print(e)


if __name__ == "__main__":
    get_area_zufang_info('sz','南山区','大新')