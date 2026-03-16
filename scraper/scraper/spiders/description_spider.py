import scrapy
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup

class Spider(scrapy.Spider):
    name = "description"

    def __init__(self, start_urls):
        super().__init__()
        self.start_urls = start_urls

    def parse(self, response):
        yield BeautifulSoup(response.body, "html.parser").select_one("section.description").prettify()

class ScraperRun:
    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.items = []
        dispatcher.connect(self.crawler_results, signal=scrapy.signals.item_scraped)

    def crawler_results(self, signal, sender, item, response, spider):
        self.items.append(item)

    def run_spider(self):
        settings = get_project_settings()
        process = CrawlerProcess(settings=settings)
        process.crawl(Spider, start_urls=self.start_urls)
        process.start()
        return self.items

if __name__ == "__main__":
    import os
    import json

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open("../../posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
        soups = list(BeautifulSoup(html_doc, "html.parser") for html_doc in posts)
        start_urls = list(soup.select_one("a.base-card__full-link").get("href") for soup in soups)

    scraper = ScraperRun(start_urls=start_urls)
    results = scraper.run_spider()

    with open("../../descriptions.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
