from abc import abstractmethod

import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']

    search_name = input('Введите запрос для поиска книг:')
    start_urls = [f'https://www.labirint.ru/search/{search_name}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']/a[@class = 'pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class = 'product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    @abstractmethod
    def book_parse(self, response: HtmlResponse):

        name = response.xpath("//h1/text()").get()
        autor = response.xpath("//div[contains(text(), 'Автор: ' )]/a/@data-event-content").getall()
        price = response.xpath("//div[@class = 'buying']//span[contains(@class, 'buying') "
                               "and contains(@class, 'number')]/text()").getall()
        rating = response.xpath("//div[@id='rate']/text()").get()
        url = response.url

        yield BookparserItem(name=name, autor=autor, full_price=price, rating=rating, url=url)

