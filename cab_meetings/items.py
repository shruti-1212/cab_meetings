import scrapy

class CabMinutesItem(scrapy.Item):
    date = scrapy.Field()
    meeting_title = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()

