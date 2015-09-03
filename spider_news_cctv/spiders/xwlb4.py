# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy import log
import threading
import MySQLdb
from datetime import date, timedelta
import re
from spider_news_cctv.items import SpiderNewsCctvItem

class Xwlb4Spider(scrapy.Spider):
    name = "xwlb4"
    allowed_domains = ["www.cctv.com"]
    start_urls = (
        'http://www.cctv.com/news/xwlb/20070831/index.shtml',
    )

    FLAG_INTERRUPT = False
    SELECT_NEWS_XWLB_BY_TITLE = "SELECT * FROM news_xwlb WHERE title='%s'"

    lock = threading.RLock()
    conn=MySQLdb.connect(user='root', passwd='123123', db='news', autocommit=True)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    URL_TEMPLATE = 'http://www.cctv.com/news/xwlb/%s/index.shtml'
    day = timedelta(1)
    now = date(2009, 6, 25)

    def is_news_not_saved(self, title):
        if self.FLAG_INTERRUPT:
            self.lock.acquire()
            rows = self.cursor.execute(self.SELECT_NEWS_XWLB_BY_TITLE % (title))
            if rows > 0:
                log.msg("XWLB news saved all finished.", level=log.INFO)
                return False
            else:
                return True
            self.lock.release()
        else:
            return True

    def parse_news(self, response):
        log.msg("Start to parse news " + response.url, level=log.INFO)
        item = SpiderNewsCctvItem()
        day = title = keywords = url = article = ''
        url = response.url
        day = response.meta['day']
        title = response.meta['title']
        response = response.body
        soup = BeautifulSoup(response)
        try:
            items_keywords = soup.find(class_='tags dot_x_t').find_all('li')
            for i in range(0, len(items_keywords)):
                keywords += items_keywords[i].text.strip()
        except:
            log.msg("News " + title + " dont has keywords!", level=log.INFO)
        try:
            article = soup.find(class_='style_p2').text.strip()
        except:
            log.msg("News " + title + " dont has article!", level=log.INFO)
        item['title'] = title
        item['day'] = day
        item['url'] = url
        item['keywords'] = keywords
        item['article'] = article
        return item

    def parse(self, response):
        str_now = self.now.strftime('%Y%m%d')
        self.now = self.now - self.day
        next_parse = []
        if (str_now == '20070830'):
            pass
        else:
            if self.now != (date(2009, 6, 25) - self.day):
                try:
                    items = response.selector.xpath('//a[contains(@href, "http://news.cctv.com/xwlb")]').extract()
                    for i in range(1, len(items)):
                        soup = BeautifulSoup(items[i])
                        item_url = soup.a['href']
                        title = soup.a.text.strip()
                        if not self.is_news_not_saved(title):
                            return next_parse
                        next_parse.append(self.make_requests_from_url(item_url).replace(callback=self.parse_news, meta={'day': (self.now + self.day).strftime('%Y%m%d'), 'title': title}))
                except:
                    log.msg("Page " + response.url + " parse error!", level=log.ERROR)
            url = self.URL_TEMPLATE % self.now.strftime('%Y%m%d')
            log.msg("Start to parse page " + url, level=log.INFO)
            next_parse.append(self.make_requests_from_url(url))
            return next_parse
