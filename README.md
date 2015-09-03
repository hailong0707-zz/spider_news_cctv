##README

-------------------------------

- 当前的`settings.py`经过调试相对比较稳定，不要轻易修改！！！
- 当前，所有爬虫**增量**抓取的开关已经打开，如果需要，可以手动关闭，`/spiders/***.py`文件的`FLAG_INTERRUPT = True`常量

- 20110406 ~ 20130715 ~ now `scrapy crawl xwlb` http://cctv.cntv.cn/lm/xinwenlianbo/20110406.shtml
- 20100613 ~ 20110405 `scrapy crawl xwlb1` http://news.cntv.cn/program/xwlb/20100613.shtml
- 20100506 ~ 20100612 `scrapy crawl xwlb2` http://news.cntv.cn/program/xwlb/20100506.shtml
- 20090626 ~ 20100505 `scrapy crawl xwlb3` http://news.cctv.com/program/xwlb/20090626.shtml
- 20070831 ~ 20090625 `scrapy crawl xwlb4` http://www.cctv.com/news/xwlb/20070831/index.shtml

//还存在无法解析的网页
- 20061012 ~ 20070814 ~ 20070830 `scrapy crawl xwlb5` 20070814无法解析 http://www.cctv.com/news/xwlb/20061012/index.shtml
- 20050609 ~ 20061011 解析方式与20061012 ~ 20070830一致,合并 http://www.cctv.com/news/xwlb/20050609/index.shtml

- 20020908 ~ 20050608 `scrapy crawl xwlb6` http://www.cctv.com/news/xwlb/20020908/index.shtml
- 如果有问题，可以发邮件沟通`hailong0707@gmail.com`
