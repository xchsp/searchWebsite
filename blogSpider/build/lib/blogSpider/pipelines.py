# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import pymongo

from scrapy.exporters import JsonItemExporter
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class ElasticSearchPipeline(object):

    def process_item(self, item, spider):
        item.save_to_elastic()

        return item


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg("data added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def sipder_close(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('article-export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class BlogspiderPipeline(object):
    def process_item(self, item, spider):
        return item
