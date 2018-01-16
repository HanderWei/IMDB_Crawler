# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    id = scrapy.Field()         # id
    title = scrapy.Field()      # 电影名
    rank = scrapy.Field()       # 排名
    img_url = scrapy.Field()    # 缩略图URL
    link = scrapy.Field()       # 链接
