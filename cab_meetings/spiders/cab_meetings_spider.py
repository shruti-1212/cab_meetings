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
        try:
            # Extract all links under the content core
            rows = response.xpath('//div[@id="content-core"]//a')
            if not rows:
                self.logger.warning("No document links found on the page.")

            for row in rows:
                item = CabMinutesItem()

                try:
                    date_raw = row.xpath('text()').get()
                    if not date_raw:
                        self.logger.warning("No date text found in a link.")
                        continue

                    words = date_raw.split()
                    if not words:
                        self.logger.warning(f"Empty date string found: '{date_raw}'")
                        continue

                    # Determine date part for parsing
                    date_part = " ".join(words[:-1]) if not words[-1].isnumeric() else date_raw
                    try:
                        item['date'] = parser.parse(date_part).strftime('%Y-%m-%d')
                    except Exception as e:
                        self.logger.error(f"Failed to parse date '{date_part}': {e}")
                        item['date'] = ""

                    # Get meeting title, avoid absolute XPath inside loop
                    doc_title = row.xpath('text()').get() or ""
                    page_title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get() or ""
                    item['meeting_title'] = doc_title + " " + page_title

                    # Set category based on last word numeric check
                    item['category'] = "other" if not words[-1].isnumeric() else "minutes"

                    url = row.xpath('@href').get()
                    if not url:
                        self.logger.warning(f"No URL found for document titled '{doc_title}'")
                        continue

                    # Make URL absolute if relative
                    item['url'] = response.urljoin(url)

                    yield item

                except Exception as e:
                    self.logger.error(f"Error processing a document link: {e}")

        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
