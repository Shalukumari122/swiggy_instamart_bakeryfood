# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SwiggyInstamartBakeryfoodItem(scrapy.Item):
    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = scrapy.Field()


class SwiggyInstamartBakeryfoodItem1(scrapy.Item):
    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = scrapy.Field()
