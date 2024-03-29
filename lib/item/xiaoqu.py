#!/usr/bin/env python
# coding=utf-8


class XiaoQu(object):
    def __init__(self, district, area, name, price, on_sale):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.on_sale = on_sale

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.on_sale
