import scrapy
from scrapy import Request
from imdb_crawler.items import MovieItem


class Top250Spiders(scrapy.Spider):
    name = "top_250"
    allowed_domains = ['imdb.com']
    start_urls = [
        'http://www.imdb.com/chart/top'
    ]
    base_url = 'http://www.imdb.com'

    def parse(self, response):
        movies = response.xpath('//tbody/tr')
        for movie in movies:
            rank = movie.xpath('td[@class="posterColumn"]/span[@name="rk"]/@data-value').extract()
            title = movie.xpath('td[@class="titleColumn"]/a/text()').extract()
            url = movie.xpath('td[@class="posterColumn"]/a/@href').extract()
            movie_url = self.base_url + url[0]
            meta = {"rank": rank[0], "title": title[0], "link": movie_url}
            yield Request(movie_url, meta=meta, callback=self.parse_movie)

    def parse_movie(self, response):
        movie_item = MovieItem()
        movie_item['rank'] = response.meta['rank']
        movie_item['title'] = response.meta['title']
        movie_item['link'] = response.meta['link']
        movie_item['poster'] = response.xpath('//div[@class="poster"]/a/img/@src').extract()[0]
        movie_item['year'] = response.xpath('//*[@id="titleYear"]/a/text()').extract()[0]
        movie_item['ratingValue'] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
        movie_item['ratingCount'] = response.xpath('//span[@itemprop="ratingCount"]/text()').extract()[0]
        movie_item['genre'] = response.xpath('//span[@itemprop="genre"]/text()').extract()
        movie_item['director'] = response.xpath(
            '//div[@class="credit_summary_item"]/h4[text()="Director:"]/following-sibling::span/a/span/text()').extract()
        movie_item['writers'] = response.xpath(
            '//div[@class="credit_summary_item"]/h4[text()="Writers:"]/following-sibling::span/a/span/text()').extract()
        movie_item['actors'] = response.xpath('//td[@itemprop="actor"]//span[@itemprop="name"]/text()').extract()
        movie_item['country'] = response.xpath(
            '//*[@id="titleDetails"]/div/h4[text()="Country:"]/following-sibling::a/text()').extract()
        movie_item['language'] = response.xpath(
            '//*[@id="titleDetails"]/div/h4[text()="Language:"]/following-sibling::a/text()').extract()
        movie_item['runtime'] = response.xpath(
            '//*[@id="titleDetails"]/div/h4[text()="Runtime:"]/following-sibling::time/text()').extract()
        # 存在为空的可能
        movie_item['sound_mix'] = \
            response.xpath('//*[@id="titleDetails"]/div/h4[text()="Sound Mix:"]/following-sibling::a/text()').extract()
        movie_item['color'] = \
            response.xpath('//*[@id="titleDetails"]/div/h4[text()="Color:"]/following-sibling::a/text()').extract()[0]
        # 存在为空的可能
        movie_item['aspect_ratio'] = \
            response.xpath(
                '//*[@id="titleDetails"]/div/h4[text()="Aspect Ratio:"]/following-sibling::text()').extract()
        yield movie_item
