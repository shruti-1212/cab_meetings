import scrapy
from cab_meetings.items import CabMinutesItem
from dateutil import parser

class CabSpider(scrapy.Spider):
    name = "cab"
    allowed_domains = ["codot.gov"]
    start_urls = [
        "https://www.codot.gov/programs/aeronautics/colorado-aeronautical-board/cab-meeting-minutes-1"
    ]

    def parse(self, response):
        # Extract rows using XPath
        rows = response.xpath('//div[@id="content-core"]//a')
        for row in rows:
            item = CabMinutesItem()
            date_raw = row.xpath('text()').get()

            words = date_raw.split()
            date_part = " ".join(words[:-1]) if not words[-1].isnumeric() else date_raw
            item['date'] = parser.parse(date_part).strftime('%Y-%m-%d')
            item['meeting_title'] = date_raw + " " + row.xpath('//h1[@class="documentFirstHeading"]//text()').get()
            item['category'] = "other" if not words[-1].isnumeric() else "minutes"
            item['url'] = row.xpath('@href').get()

            yield item

