# -*- coding: utf-8 -*-
import json
import logging

import scrapy
from scrapy import log
from old_house.items import city_status_Item
from scrapy.selector import Selector
from scrapy.http import Request
import time


class shenyang_house_spider(scrapy.Spider):
    name = "reset"
    start_urls = [
        "http://www.anjuke.com/sy-city.html"
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'old_house.pipelines.StatusPipeline': 300,
        },
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
                        next_url = url[0] + '/sale/'
                        yield Request(next_url, callback=self.country_parse, meta={"city": city})
                    else:
                        break

    def country_parse(self, response):

        city = response.meta["city"]
        log.msg("city " + city + " into country parse")
        sel = Selector(response)
        counties = sel.xpath('//div[@class="items"][1]/span[@class="elems-l"]/a')
        for county in counties:
            county_url = county.xpath('@href').extract()[0].encode("utf-8")
            county_name=county.xpath('text()').extract()[0].encode("utf-8")
            yield Request(county_url, callback=self.place_parse, meta={"city": city,"county":county_name})

    def place_parse(self, response):
        city = response.meta["city"]
        county=response.meta["county"]
        log.msg("city " + city + " into place parse")
        sel = Selector(response)
        places = sel.xpath('//div[@class="items"][1]/span[@class="elems-l"]/div[@class="sub-items"]/a')
        for place in places:
            url = place.xpath('@href').extract()[0].encode("utf-8")
            place_name=place.xpath('text()').extract()[0].encode("utf-8")
            item=city_status_Item()
            item["city"]=city
            item["county"]=county
            item["place"]=place_name
            item["url"]=url
            yield item
