from decimal import Decimal

import pymongo
from bson import Decimal128


class MongoDBPipeline(object):
    collection_name = 'items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        collection_name = getattr(spider, 'collection_name')
        if collection_name:
            self.collection_name = collection_name

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # TODO => Have settings or function in spider to activate update_or_create behavior

        item_dict = dict(item)
        for key, value in item_dict.items():
            if isinstance(value, Decimal):
                item_dict[key] = Decimal128(value)

        self.db[self.collection_name].insert_one(item_dict)
        return item
