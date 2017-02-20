# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import logging
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class OldHousePipeline(object):
    def __init__(self):
        conn = MySQLdb.connect(
            host='#####',
            port=3306,
            user='spider',
            passwd='spider',
            db='HouseProperty',
            charset='utf8'
        )
        self.conn = conn
        
    def process_item(self,item,spider):

        try:
            self.conn.ping()
        except:
            self.conn.ping(True)

        cur = self.conn.cursor()
        sql="insert into old_house_info (city,name,area,price,avg_price,county,place,address,type,date) values ('"+str(item['city'])+"','"\
+str(item['name'])+"','"\
+str(item['area'])+"','"\
+str(item['price'])+"','"\
+str(item['avg_price'])+"','"\
+str(item['county'])+"','"\
+str(item['place'])+"','"\
+str(item['address'])+"','"\
+str(item['house_type'])+"','"\
+str(item['date'])+"')"
        try:
            # 执行sql语句
            cur.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except Exception, e:
            log.msg("mysql erro " + str(e),_level=logging.ERROR)
        cur.close()
        return item
    def __del__(self):
        self.conn.close()


class AVGPricePipeline(object):
    def __init__(self):
        conn = MySQLdb.connect(
            host='######',
            port=3306,
            user='spider',
            passwd='spider',
            db='HouseProperty',
            charset='utf8'
        )
        self.conn = conn

    def process_item(self, item, spider):

        try:
            self.conn.ping()
        except:
            self.conn.ping(True)


        if item["type"]=="city":
            key=item["city"]+item["year"]+item["month"]
            cur = self.conn.cursor()
            sql="select * from city_avg_price where PKey='"+key+"'"
            cur.execute(sql)
            rows = cur.fetchall()
            # 提交到数据库执行
            self.conn.commit()
            if len(rows)==0:
                sql = "insert into city_avg_price (PKey,city,year,month,price) values ('"+key+"','" + str(
                    item['city']) + "','" \
                    + str(item['year']) + "','" \
                    + str(item['month']) + "'," \
                    + str(item['price']) + ")"
                try:
                    # 执行sql语句
                    cur.execute(sql)
                    # 提交到数据库执行
                    self.conn.commit()
                except Exception, e:
                    log.msg("mysql erro " + str(e), _level=logging.ERROR)
            cur.close()
            return item
        if item["type"]=="county":
            key = item["city"] + item["county"]+item["year"] + item["month"]
            cur = self.conn.cursor()
            sql = "select * from county_avg_price where PKey='" + key + "'"
            cur.execute(sql)
            rows = cur.fetchall()
            # 提交到数据库执行
            self.conn.commit()
            if len(rows) == 0:
                sql = "insert into county_avg_price (PKey,city,county,year,month,price) values ('"+key+"','" + str(
                    item['city']) + "','" \
                      + str(item['county']) + "','" \
                      + str(item['year']) + "','" \
                    + str(item['month']) + "'," \
                    + str(item['price']) + ")"
                try:
                    # 执行sql语句
                    cur.execute(sql)
                    # 提交到数据库执行
                    self.conn.commit()
                except Exception, e:
                    log.msg("mysql erro " + str(e), _level=logging.ERROR)
            cur.close()
            return item

        if item["type"]=="place":
            key = item["city"]+item["county"]+item["place"]+item["year"] + item["month"]
            cur = self.conn.cursor()
            sql = "select * from place_avg_price where PKey='" + key + "'"
            cur.execute(sql)
            rows = cur.fetchall()
            # 提交到数据库执行
            self.conn.commit()
            if len(rows) == 0:
                sql = "insert into place_avg_price (PKey,city,county,place,year,month,price) values ('"+key+"','" + str(
                    item['city']) + "','" \
                      + str(item['county']) + "','" \
                      + str(item['place']) + "','" \
                      + str(item['year']) + "','" \
                    + str(item['month']) + "'," \
                    + str(item['price']) + ")"
                try:
                    # 执行sql语句
                    cur.execute(sql)
                    # 提交到数据库执行
                    self.conn.commit()
                except Exception, e:
                    log.msg("mysql erro " + str(e), _level=logging.ERROR)
            cur.close()
            return item

    def __del__(self):
        self.conn.close()


class StatusPipeline(object):
    def __init__(self):
        conn = MySQLdb.connect(
            host='#######',
            port=3306,
            user='spider',
            passwd='spider',
            db='HouseProperty',
            charset='utf8'
        )
        self.conn = conn

    def process_item(self, item, spider):

        try:
            self.conn.ping()
        except:
            self.conn.ping(True)

        cur = self.conn.cursor()
        sql = "insert into status (city,county,url,place,status) values ('" + str(
            item['city']) + "','" \
              + str(item['county']) + "','" \
              + str(item['url']) + "','" \
              + str(item['place']) + "','undo')"
        try:
            # 执行sql语句
            cur.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except Exception, e:
            log.msg("mysql erro " + str(e), _level=logging.ERROR)
        cur.close()
        return item

    def __del__(self):
        self.conn.close()

class HousePipeline(object):
    def __init__(self):
        conn = MySQLdb.connect(
            host='#######',
            port=3306,
            user='spider',
            passwd='spider',
            db='HouseProperty',
            charset='utf8'
        )
        self.conn = conn

    def process_item(self,item,spider):

        try:
            self.conn.ping()
        except:
            self.conn.ping(True)

        cur = self.conn.cursor()
        sql="select * from house_info where Pkey='"+item["key"]+"' "
        cur.execute(sql)
        rows=cur.fetchall()
        self.conn.commit()
        if len(rows)==0:
            sql="insert into house_info (Pkey,city,name,area,price,avg_price,county,place,address,type,date) values ('"+str(item['key'])+"','"\
            +str(item['city'])+"','" \
            + str(item['name']) + "','" \
            +str(item['area'])+"','"\
            +str(item['price'])+"','"\
            +str(item['avg_price'])+"','"\
            +str(item['county'])+"','"\
            +str(item['place'])+"','"\
            +str(item['address'])+"','"\
            +str(item['house_type'])+"','"\
            +str(item['date'])+"')"
            try:
                # 执行sql语句
                cur.execute(sql)
                # 提交到数据库执行
                self.conn.commit()
            except Exception, e:
                log.msg("mysql erro " + str(e),_level=logging.ERROR)
        else:
            log.msg("has crawled this house name:"+item["name"]+"  city:"+item["city"]+"  key:"+item["key"]+"  ")
        cur.close()
        return item
    def __del__(self):
        self.conn.close()