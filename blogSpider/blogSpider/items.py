# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from .es_model import ElasticType
from .utils import date_convert, gen_suggest


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class FreebufItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    html_content = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )

    def save_to_elastic(self):
        items = ElasticType()
        items.url = self['url']
        items.title = self['title'].strip('\r\n')
        items.author = self['author']
        items.html_content = self['html_content']
        # items.create_time = self['create_time']
        items.suggest = gen_suggest(ElasticType._doc_type.index, items.title)

        items.save()
        return


class BlogspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
