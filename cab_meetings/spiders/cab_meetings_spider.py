import scrapy
from cab_meetings.items import CabMinutesItem
from dateutil import parser

class CabSpider(scrapy.Spider):
    name = 'cab'
    allowed_domains = ['codot.gov']
    start_urls = [
        'https://www.codot.gov/programs/aeronautics/colorado-aeronautical-board/cab-meeting-minutes-1'
    ]

    def parse(self, response):
        rows = response.xpath('//table//tr')[1:]  # Skip header row

        for row in rows:
            item = CabMinutesItem() 
            title = row.xpath('./td[1]//text()').get(default='').strip()
            date_str = row.xpath('./td[2]//text()').get(default='').strip()
            link = row.xpath('.//a/@href').get()

            if not title or not link:
                continue

            # Date conversion
            try:
                parsed_date = parser.parse(date_str)
                item['date'] = parsed_date.strftime('%Y-%m-%d')
            except Exception:
                item['date'] = ''

            item['meeting_title'] = title
            item['url'] = response.urljoin(link)

            # Determine category
            if 'minutes' in title.lower():
                item['category'] = 'minutes'
            else:
                item['category'] = 'other'

            yield item

        # # Follow pagination to second page (if exists)
        # next_page = response.xpath('//a[contains(text(),"Next")]/@href').get()
        # if next_page and 'page=2' in next_page:
        #     yield response.follow(next_page, callback=self.parse)
