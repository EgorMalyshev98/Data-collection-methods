# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books_labirint

    def process_item(self, item, spider):
        item['full_price'], item['discount_price'] = self.process_price(item['full_price'])
        item['rating'] = float(item['rating'])
        collection = self.mongo_base['books']
        collection.insert_one(item)
        return item

    def process_price(self, price):

        if len(price) == 2:
            f_price = int(price[0])
            d_price = int(price[1])
        else:
            f_price = int(price[0])
            d_price = None
        return f_price, d_price
