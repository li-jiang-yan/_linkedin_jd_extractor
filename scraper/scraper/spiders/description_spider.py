import scrapy
from bs4 import BeautifulSoup

class Spider(scrapy.Spider):
    name = "description"

    def __init__(self, start_urls, results=None):
        super().__init__()
        self.start_urls = start_urls
        self.results = results if results is not None else []

    def parse(self, response):
        self.results.append(BeautifulSoup(response.body, "html.parser").select_one("section.description").prettify())

if __name__ == "__main__":
    import os
    import json

    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    from scrapy.utils.reactor import install_reactor

    # Install the reactor BEFORE importing twisted.internet.reactor
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    from twisted.internet import reactor, defer

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    results = []

    with open("../../posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
        soups = list(BeautifulSoup(html_doc, "html.parser") for html_doc in posts)
        start_urls = list(soup.select_one("a.base-card__full-link").get("href") for soup in soups)

    @defer.inlineCallbacks
    def crawl():
        runner = CrawlerRunner(get_project_settings())
        yield runner.crawl(Spider, start_urls=start_urls, results=results)
        reactor.stop()

    crawl()
    reactor.run()

    with open("../../descriptions.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
