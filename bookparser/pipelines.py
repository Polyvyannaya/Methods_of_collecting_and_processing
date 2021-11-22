# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.books_db = client["books"]

    def process_item(self, item, spider):
        item['author'] = self.process_author(item['author'])
        item['name'] = self.process_name(item['name'])
        item['_id'] = item['url']

        collection = self.books_db[spider.name]
        collection.insert_one(item)
        return item

    def process_author(self, author):
        if not author:
            author_name = None
        else:
            author_name = author[1]
        return author_name

    def process_name(self, name):
        if (': ' in name):
            name_str = name.split(': ')[1]
        else:
            name_str = name
        return name_str

