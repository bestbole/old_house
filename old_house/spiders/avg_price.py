# -*- coding: utf-8 -*-
import json
import logging
import scrapy
from scrapy import log
from old_house.items import city_price_Item,county_price_Item,place_price_Item
from scrapy.selector import Selector
from scrapy.http import Request
import time


class shenyang_house_spider(scrapy.Spider):
    name = "AVG"
    start_urls = [
         "http://www.anjuke.com/sy-city.html"

    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'old_house.pipelines.AVGPricePipeline': 300,
        }
    }
    allowed_domains = ["anjuke.com"]

    def parse(self, response):
        sel = Selector(response)
        for x in range(1, 3):
            for i in range(1, 12):
                for k in range(1, 39):
                    xpathStr = '//*[@id="content"]/div[4]/div[' + str(x) + ']/dl[' + str(i) + ']/dd/a[' + str(k) + ']'
                    url = sel.xpath(xpathStr + '/@href').extract()
                    citypath = sel.xpath(xpathStr + '/text()').extract()
                    if url != []:
                        city = citypath[0].encode("utf-8")
                        log.msg("url:" + url[0])
                        log.msg("city:" + city)
                        next_url = url[0].replace(".fang.",".")+'/market/'
                        yield Request(next_url, callback=self.city_parse, meta={"city": city})
                    else:
                        break
        # yield Request(url="http://shenyang.anjuke.com/market/", callback=self.city_parse, meta={"city": "沈阳"})

    def city_parse(self, response):

        city = response.meta["city"]
        log.msg("city " + city + " into county parse")

        sel = Selector(response)


        # counties = sel.xpath('//div[@class="area"]/div[@class="bigArea"]/a')
        # for county in counties[1:]:
        #     county_url = county.xpath('@href').extract()[0].encode("utf-8")
        #     # print "abcd     "+county_url
        #     county_name=county.xpath('text()').extract()[0].encode("utf-8")
        #     yield Request(county_url, callback=self.county_parse, meta={"city": city,"county":county_name})
        #
        #
        js=sel.xpath("//script[5]/text()").extract()[0].split("J.ready(function(){")[2].split("drawChart(")[1]\
            .split(");")[0]\
            .replace(" ","").replace("id:","\"id\":").replace("type:","\"type\":").replace("xdata:","\"xdata\":")\
            .replace("xyear:","\"xyear\":").replace("ydata:","\"ydata\":").replace("'","\"")
        data=json.loads(js)
        for i in range(len(data["xdata"])):
            item = city_price_Item()
            item["type"] = "city"
            item["city"]=city
            month=data["xdata"][i]
            item["month"]=month.encode("utf-8")
            item["year"]=data["xyear"][month].encode("utf-8")
            item["price"]=str(data["ydata"][0]["data"][i])
            yield item



    def county_parse(self, response):
        city = response.meta["city"]
        county=response.meta["county"]
        log.msg("city " + city + " into place parse")

        sel = Selector(response)

        places = sel.xpath('//div[@class="area"]/div[@class="smallArea"]/a')
        for place in places[1:]:
            url = place.xpath('@href').extract()[0].encode("utf-8")
            place_name = place.xpath('text()').extract()[0].encode("utf-8")
            yield Request(url, callback=self.place_parse, meta={"city": city,"county":county,"place":place_name})


        js = sel.xpath("//script[5]/text()").extract()[0].split("J.ready(function(){")[2].split("drawChart(")[1]\
            .split(");")[0].replace(" ", "").replace("id:", "\"id\":").replace("type:", "\"type\":").replace(
            "xdata:", "\"xdata\":") \
            .replace("xyear:", "\"xyear\":").replace("ydata:", "\"ydata\":").replace("'", "\"")
        data = json.loads(js)
        for i in range(len(data["xdata"])):
            item = city_price_Item()
            item["type"] = "county"
            item["city"] = city
            item["county"]=county
            month = data["xdata"][i]
            item["month"] = month.encode("utf-8")
            item["year"] = data["xyear"][month].encode("utf-8")
            item["price"] = str(data["ydata"][0]["data"][i])
            yield item


    def place_parse(self, response):
        log.msg("get into " + response.url)
        city = response.meta["city"]
        county = response.meta["county"]
        place=response.meta["place"]

        sel = Selector(response)
        js = sel.xpath("//script[5]/text()").extract()[0].split("J.ready(function(){")[2].split("drawChart(")[1] \
            .split(");")[0].replace(" ", "")\
            .replace("id:", "\"id\":").replace("type:", "\"type\":").replace(
            "xdata:", "\"xdata\":") \
            .replace("xyear:", "\"xyear\":").replace("ydata:", "\"ydata\":").replace("'", "\"")
        # log.msg(js)
        data = json.loads(js)
        for i in range(len(data["xdata"])):
            item = city_price_Item()
            item["type"] = "place"
            item["city"] = city
            item["county"] = county
            item["place"]=place
            month = data["xdata"][i]
            item["month"] = month.encode("utf-8")
            item["year"] = data["xyear"][month].encode("utf-8")
            item["price"] = str(data["ydata"][0]["data"][i])
            yield item

