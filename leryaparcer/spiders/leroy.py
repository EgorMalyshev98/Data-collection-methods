from abc import abstractmethod

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leryaparcer.items import LeryaparcerItem

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("search")}']
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='next i-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeryaparcerItem(), response=response)
        loader.add_xpath('price', "//span[@class='regular-price']/span[@class='price']//span/text()")
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//div[@class='product-media__thumbs']//img/@src")
        loader.add_value('url', response.url)

        yield loader.load_item()


