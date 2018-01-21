# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # 电影名
    title = scrapy.Field()
    # 排名
    rank = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 图片
    # //div[@class="poster"]/a/img/@src
    poster = scrapy.Field()
    # 年份
    # //*[@id="titleYear"]/a/text()
    year = scrapy.Field()
    # 评分
    # //span[@itemprop="ratingValue"]/text()
    ratingValue = scrapy.Field()
    # 评价人数
    # //span[@itemprop="ratingCount"]/text()
    ratingCount = scrapy.Field()
    # 类型
    # //span[@itemprop="genre"]/text()
    genre = scrapy.Field()
    # 导演
    # //div[@class="credit_summary_item"]/h4[text()="Director:"]/following-sibling::span/a/span/text()
    director = scrapy.Field()
    # 编剧
    # //div[@class="credit_summary_item"]/h4[text()="Writers:"]/following-sibling::span/a/span/text()
    writers = scrapy.Field()
    # 演员
    # //td[@itemprop="actor"]//span[@itemprop="name"]/text()
    actors = scrapy.Field()
    # 国家
    # //*[@id="titleDetails"]/div/h4[text()="Country:"]/following-sibling::a/text()
    country = scrapy.Field()
    # 语言
    # //*[@id="titleDetails"]/div/h4[text()="Language:"]/following-sibling::a/text()
    language = scrapy.Field()
    # 时长
    # //*[@id="titleDetails"]/div/h4[text()="Runtime:"]/following-sibling::time/text()
    runtime = scrapy.Field()
    # 音效
    # //*[@id="titleDetails"]/div/h4[text()="Sound Mix:"]/following-sibling::a/text()
    sound_mix = scrapy.Field()
    # 色彩
    # //*[@id="titleDetails"]/div/h4[text()="Color:"]/following-sibling::a/text()
    color = scrapy.Field()
    # 长宽比
    # //*[@id="titleDetails"]/div/h4[text()="Aspect Ratio:"]/following-sibling::text()
    aspect_ratio = scrapy.Field()
