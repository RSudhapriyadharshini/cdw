# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CdwItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    sku = scrapy.Field()
    cdw_part_number = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    short_description = scrapy.Field()
    base_image = scrapy.Field()
    thumbnail_image = scrapy.Field()
    categories = scrapy.Field()

