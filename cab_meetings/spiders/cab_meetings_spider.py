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
            date = parser.parse(date_raw).strftime('%Y-%m-%d')
            title = date_raw + " " + row.xpath('//h1[@class="documentFirstHeading"]//text()').get()
            category = date_raw.split()[-1] if date_raw.lower() == 'minutes' else 'other'
            doc_link = row.xpath('@href').get()

            print(date)
            print(title)
            print(category)
            print(doc_link)
            input("__________________________________________")

            yield item

