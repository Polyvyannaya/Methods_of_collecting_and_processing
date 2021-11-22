import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0']

    def parse(self, response: HtmlResponse):
       next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
       if next_page:
           yield response.follow(next_page, callback=self.parse)

       links = response.xpath("//a[@class='product-title-link']/@href").getall()
       for link in links:
           yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        author = response.xpath('//div[@class="authors"]//text()').getall()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        price_old = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        price_sale = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rate = response.xpath("//div[@id='rate']/text()").get()
        url = response.url
        yield BookparserItem(name=name, author=author, price=price, price_old=price_old, price_sale=price_sale, rate=rate, url=url)

