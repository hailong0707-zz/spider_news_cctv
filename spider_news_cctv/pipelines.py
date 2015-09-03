# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import threading
import MySQLdb
from scrapy import log

class SpiderNewsCctvPipeline(object):

    INSERT_NEWS_XWLB = ("INSERT INTO news_xwlb (title, day, url, keywords, article) "
                        "VALUES (%s, %s, %s, %s, %s)")

    lock = threading.RLock()
    conn=MySQLdb.connect(user='root', passwd='123123', db='news', autocommit=True)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    def insert(self, title, day, url, keywords, article):
        self.lock.acquire()
        news = (title, day, url, keywords, article)
        try:
            self.cursor.execute(self.INSERT_NEWS_XWLB, news)
            log.msg(title + " saved successfully", level=log.INFO)
        except:
            log.msg("MySQL exception !!!", level=log.ERROR)
        self.lock.release()

    def process_item(self, item, spider):
        title = item['title']
        day = item['day']
        url = item['url']
        keywords = item['keywords']
        article = item['article']
        self.insert(title, day, url, keywords, article)
        return item
