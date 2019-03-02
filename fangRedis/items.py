# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class FangredisItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class NewHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()

class EsfItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
