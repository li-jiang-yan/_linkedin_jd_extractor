from itertools import chain
from urllib.parse import quote
import scrapy
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup

class Spider(scrapy.Spider):
    name = "posts"

    def __init__(self, keywords, location, number):
        super().__init__()
        self.start_urls = list(f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={quote(keywords)}&location={quote(location)}&start={start}" for start in range(0, int(number), 25))

    def parse(self, response):
        yield list(BeautifulSoup(html_doc, "html.parser").prettify() for html_doc in response.css("div.base-card").getall())

class ScraperRun:
    def __init__(self, keywords="Computer Science", location="Singapore", number=10):
        self.keywords = keywords
        self.location = location
        self.number = number
        self.items = []
        dispatcher.connect(self.crawler_results, signal=scrapy.signals.item_scraped)

    def crawler_results(self, signal, sender, item, response, spider):
        self.items.append(item)

    def run_spider(self):
        settings = get_project_settings()
        process = CrawlerProcess(settings=settings)
        process.crawl(Spider, keywords=self.keywords, location=self.location, number=self.number)
        process.start()
        return list(chain.from_iterable(self.items))

if __name__ == "__main__":
    import os
    import json

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    scraper = ScraperRun(keywords="Computer Science", location="Singapore", number=100)
    results = scraper.run_spider()

    with open("../../posts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
