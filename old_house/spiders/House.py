# -*- coding: utf-8 -*-
import json
import logging

import MySQLdb
import scrapy
from scrapy import log
from old_house.items import HouseItem
from scrapy.selector import Selector
from scrapy.http import Request
import time


class shenyang_house_spider(scrapy.Spider):
    name = "House"
    custom_settings = {
        'ITEM_PIPELINES': {
            'old_house.pipelines.HousePipeline': 300,
        },
    }
    allowed_domains = ["anjuke.com"]
    def start_requests(self):

        conn = MySQLdb.connect(
            host='#######',
            port=3306,
            user='spider',
            passwd='spider',
            db='HouseProperty',
            charset='utf8'
        )

        cur = conn.cursor()
        sql="select city,county,place,url from status where status='undo'"
        cur.execute(sql)
        rows = cur.fetchall()
        for i in range(0,min(len(rows),5)):
            row=rows[i]
            city=row[0].encode("utf-8")
            county=row[1].encode("utf-8")
            place=row[2].encode("utf-8")
            url=row[3].encode("utf-8")
            yield Request(url, callback=self.house_parse, meta={"city": city, "county":county, "place":place})
            sql="update status set status='doing' where url='"+url+"' "
            cur.execute(sql)
            conn.commit()
        cur.close()
        conn.close()

    def house_parse(self, response):
        log.msg("get into " + response.url)
        city = response.meta["city"]
        county=response.meta["county"]
        place=response.meta["place"]
        sel = Selector(response)
        houses = sel.xpath('//div[@class="sale-left"]/ul[@id="houselist-mod"]/li')
        for house in houses:
            item = HouseItem()
            item["city"] = city
            info = house.xpath('div[@class="house-details"]')
            key_url = info.xpath('div[1]/a[1]/@href').extract()[0].encode("utf-8").replace("http://","")
            citypy=key_url.split(".anjuke")[0]
            k=key_url.split("view/")[1].split("?")[0]
            item["key"]=citypy+"-"+k
            house_info = info.xpath('div[2]')
            item["area"] = house_info.xpath('span[1]/text()').extract()[0].encode("utf-8").replace("平方米", "")
            item["house_type"] = house_info.xpath('span[2]/text()').extract()[0].encode("utf-8")
            item["avg_price"] = house_info.xpath('span[3]/text()').extract()[0].encode("utf-8").split("元")[0]

            place_info = info.xpath('div[3]/span/@title').extract()
            if place_info == []:
                # log.msg("no place_info " + response.url)
                continue
            place_info = place_info[0].encode("utf-8").replace(" ", "|").replace(" ", "|").replace("||", "|").replace(
                "[", "").replace("]", "").split("|")
            item["county"] = county
            item["place"] = place
            try:
                item["name"] = place_info[0]
                item["address"] = place_info[2]

            except Exception, e:
                # log.msg("place_info error " + response.url)
                continue
            price = house.xpath('div[@class="pro-price"]/span[@class="price-det"]/strong/text()').extract()
            if price == []:
                # log.msg("no price " + response.url, _level=logging.ERROR)
                continue
            item["price"] = price[0].encode("utf-8")
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item["date"] = str(date)
            yield item

        next = sel.xpath('//a[@class="aNxt"]/@href').extract()
        log.msg("next:" + str(next))
        if next != []:
            log.msg("goto next page")
            log.msg("url: " + next[0].encode('utf-8'))
            yield Request(next[0].encode('utf-8'), callback=self.house_parse, meta={"city": city,"county":county,"place":place})
        else:
            log.msg(city +" "+county+" "+place+ " is over")
            conn = MySQLdb.connect(
                host='10.2.9.9',
                port=3306,
                user='spider',
                passwd='spider',
                db='HouseProperty',
                charset='utf8'
            )

            cur = conn.cursor()
            sql="update status set status='done' where city='"+city+"' and county='"+county+"' and place='"+place+"'"
            cur.execute(sql)
            conn.commit()

            while True:
                pro=city+county+place
                sql="update spider_lock set pro='"+pro+"' where id='lock' and pro='none'"
                cur.execute(sql)
                conn.commit()
                sql="select pro from spider_lock where id='lock'"
                cur.execute(sql)
                rows=cur.fetchall()
                result=rows[0][0]
                if pro==result:
                    sql="select city,county,place,url from status where status='undo'"
                    cur.execute(sql)
                    rows = cur.fetchall()
                    if len(rows)!=0:
                        row=rows[0]
                        city = row[0].encode("utf-8")
                        county = row[1].encode("utf-8")
                        place = row[2].encode("utf-8")
                        url = row[3].encode("utf-8")
                        yield Request(url, callback=self.house_parse,
                                      meta={"city": city, "county": county, "place": place})
                        sql = "update status set status='doing' where url='" + url + "' "
                        cur.execute(sql)
                        conn.commit()
                    sql = "update spider_lock set pro='none' where id='lock'"
                    cur.execute(sql)
                    conn.commit()
                    break
                time.sleep(1)

            cur.close()
            conn.close()
