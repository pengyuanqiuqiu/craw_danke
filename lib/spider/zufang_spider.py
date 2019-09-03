#!/usr/bin/env python
# coding=utf-8
import datetime
import threadpool
from lib.item.zufang import *
from lib.spider.base_spider import *
from lib.utility.path import *
from lib.zone.area import *
from lib.zone.city import get_city
from lib.utility.date import *
class ZuFangBaseSpider(BaseSpider):
    def __init__(self):
        self.account =0
        self.date_string = get_date_string()
        self.mutex = threading.Lock()
        self.total_num = 0
    def collect_area_zufang_data(self,city, District,area):

        district_name = area_dict.get(area, "")
        self.get_area_zufang_info(city,District,area)

        print("Finish crawl area: " + area + ", save data to ")

    def get_area_zufang_info(self,city_name, districts, area_name):
        page = 'http://www.danke.com/room/{0}/d{1}-b{2}.html'.format(city_name, districts, area_name)
        headers = create_headers()
        res =[]
        page_number =0
        try:
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            root = etree.HTML(html)
            page_number = 1
        except:
            time.sleep(2)
            print("Was a nice sleep, now let me continue...")

        while True:
            page = 'http://www.danke.com/room/{0}/d{1}-b{2}.html?page={3}'.format(city_name, districts, area_name,
                                                  page_number)
            BaseSpider.random_delay()
            try:
                print(page)
                response = requests.get(page, timeout=10, headers=headers)
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
            page_number += 1
            zufang_list =[]
            html = response.content
            page_text = response.text
            if '您查找的房源已售罄' not in page_text:
                root = etree.HTML(html)
                net_url = root.xpath('//div[@class="r_lbx_cena"]/a/@href')
                title = root.xpath('//div[@class="r_lbx_cena"]/a/@title')
                square = root.xpath('//div[@class="r_lbx_cenb"]/text()')
                square_result = []
                for i in square:
                    square_result.append(i.replace(" ", "").replace("\t", "").replace("\n", ""))
                square_result = [i for i in square_result if i != ""]
                price = root.xpath('//span[@class="ty_b"]/text()')
                price = [i.replace(" ", "").replace("\t", "").replace("\n", "") for i in price]
                picture = root.xpath('//div[@class="r_lbx"]/a/img/@src')
                for i in range(len(net_url)):
                    zufang = ZuFang(city_name, districts, area_name,net_url[i], title[i], square_result[i], price[i], picture[i],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    # global zufang_list
                    csv_file = self.today_path + "/{0}_{1}.csv".format(city_name, area_name)
                    with open(csv_file, "a+") as f:
                        print(zufang.text())
                        f.write(self.date_string + "," + zufang.text() + "\n")
                    self.save_picture(picture[i], title[i], city_name, districts, area_name)
            else:
                break

        return zufang_list

    def save_picture(self,url, title_name, city_name, districts, area_name):
        if url[0:2] == '//':
            url = 'http:' + url
        try:
            img = requests.get(url)
            picture = create_picture_path(city_name, districts, area_name)
            picture_url = picture + title_name.replace(" ", "") + ".jpg"
            if os.path.exists(picture_url):
                picture_url = picture + title_name.replace(" ", "") + str(random.randint(0, 20000)) + ".jpg"
            try:
                open(picture_url, 'wb').write(img.content)
            except Exception as e:
                print(e)
        except  Exception as e:
            print(e)

    def start(self):
        city = get_city()
        self.today_path = create_date_path("{0}/zufang".format(SPIDER_NAME), city, self.date_string)
        t1 = time.time()  # 开始计时
        districts,result = get_districts(city)
        print('City: {0}'.format(city))
        print('Districts: {0}'.format(districts))
        # 获得每个区的板块, area: 板块
        areas = list()
        paragram=list()
        for res in result:
            areas_of_district = res["area"]
            District = res["districts"]
            self.account +=1
            for area in areas_of_district:
                paragram.append(([city,District,area],None))
            #     # paragram.append(([city,District,area],None))
            #     self.collect_area_zufang_data( city, District,area)
                # self.get_area_zufang_info(city,District,area)
        # print(paragram)
        #     print('{0}: Area list:  {1}'.format(areas_of_district))
        #
        #     areas.extend(areas_of_district)
        #     # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        #     for area in areas_of_district:
        #         area_dict[area] = district
        # print("Area:", areas)
        # print("District and areas:", area_dict)

        # 准备线程池用到的参数
        # nones = [None for i in range(len(areas))]
        # city_list = [city for i in range(len(areas))]
        # args = zip(zip(city_list, areas), nones)
        # areas = areas[0: 1]

        # 针对每个板块写一个文件,启动一个线程来操作
        #
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_zufang_data, paragram)
        [pool.putRequest(req) for req in my_requests]
        # helper.commit()
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl data items.".format(t2 - t1))


if __name__ == '__main__':
    a =ZuFangBaseSpider()
    a.start()