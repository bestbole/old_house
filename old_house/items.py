# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import log

class OldHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()  # 城市
    county = scrapy.Field()  # 区县
    place = scrapy.Field()  # 位置
    address = scrapy.Field()  # 地址
    name = scrapy.Field()  # 楼盘名称
    avg_price = scrapy.Field()  # 均价
    price = scrapy.Field()  # 房价
    house_type = scrapy.Field()  # 户型
    area = scrapy.Field()  # 面积
    date = scrapy.Field()  # 采集日期

class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key=scrapy.Field()
    city = scrapy.Field()  # 城市
    county = scrapy.Field()  # 区县
    place = scrapy.Field()  # 位置
    address = scrapy.Field()  # 地址
    name = scrapy.Field()  # 楼盘名称
    avg_price = scrapy.Field()  # 均价
    price = scrapy.Field()  # 房价
    house_type = scrapy.Field()  # 户型
    area = scrapy.Field()  # 面积
    date = scrapy.Field()  # 采集日期



class city_price_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type=scrapy.Field()
    city = scrapy.Field()  # 城市
    county = scrapy.Field()  # 区县
    place = scrapy.Field()  # 位置
    year = scrapy.Field()
    month = scrapy.Field()
    price = scrapy.Field()  # 均价

class county_price_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type=scrapy.Field()
    city = scrapy.Field()  # 城市
    county = scrapy.Field()  # 区县
    year = scrapy.Field()
    month = scrapy.Field()
    price = scrapy.Field()  # 均价

class place_price_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type=scrapy.Field()
    city = scrapy.Field()  # 城市
    county = scrapy.Field()  # 区县
    place = scrapy.Field()  # 位置
    year = scrapy.Field()
    month = scrapy.Field()
    price = scrapy.Field()  # 均价

class city_status_Item(scrapy.Item):
    city=scrapy.Field()
    county=scrapy.Field()
    place=scrapy.Field()
    url=scrapy.Field()
