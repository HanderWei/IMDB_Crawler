import scrapy


class Top250Spiders(scrapy.Spider):
    name = "top_250"
    allowed_domains = ['imdb.com']
    start_urls = [
        'http://www.imdb.com/chart/top'
    ]

    def parse(self, response):
        movies = response.xpath('//tbody/tr')
        for movie in movies:
            # rank = movie.xpath('td[@class="posterColumn"]/span[@name="rk"]/@data-value').extract()
            # name = movie.xpath('td[@class="titleColumn"]/a/text()').extract()
            url = movie.xpath('td[@class="posterColumn"]/a/@href').extract()
            yield response.follow(url[0], self.parse_movie)
        #
        # filename = 'top250.txt'
        # open(filename, 'w').close()
        # with open(filename, 'a') as f:
        #     for movie in movies:
        #         rank = movie.xpath('td[@class="posterColumn"]/span[@name="rk"]/@data-value').extract()
        #         name = movie.xpath('td[@class="titleColumn"]/a/text()').extract()
        #         url = movie.xpath('td[@class="posterColumn"]/a/@href').extract()
        #         args = (rank[0], name[0])
        #         f.write("%s. %s\n" % args)
        #         f.write("http://www.imdb.com%s\n\n" % url[0])

    def parse_movie(self, response):
        title_wrapper = response.xpath('//div[@class="title_wrapper"]')
        name = title_wrapper.xpath('h1[@itemprop="name"]/text()').extract()
        filename = 'back/%s.html' % name[0].strip()
        with open(filename, 'wb') as f:
            f.write(response.body)
