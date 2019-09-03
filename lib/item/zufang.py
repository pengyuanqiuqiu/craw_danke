#!/usr/bin/env python
# coding=utf-8


class ZuFang(object):


    def __init__(self, city,district, area, net_url, title, square_result, price,picture,datetime):
        self.city = city
        self.district = district
        self.area = area
        self.net_url = net_url
        self.title = title
        self.square_result = square_result
        self.price = price
        self.picture = picture
        self.datetime = datetime

    def text(self):
        return self.city + "," + \
            self.district + "," + \
                self.area + "," + \
                self.net_url + "," + \
                self.title + "," + \
                self.square_result + "," + \
                self.price+ "," + \
               self.picture + "," + \
               self.datetime + ","
