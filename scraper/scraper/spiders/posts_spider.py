from urllib.parse import quote
import scrapy
from bs4 import BeautifulSoup

class Spider(scrapy.Spider):
    name = "posts"

    def __init__(self, keywords, location, number, results=None):
        super().__init__()
        self.start_urls = list(f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={quote(keywords)}&location={quote(location)}&start={start}" for start in range(0, int(number), 25))
        self.results = results if results is not None else []

    def parse(self, response):
        self.results.extend(BeautifulSoup(html_doc, "html.parser").prettify() for html_doc in response.css("div.base-card").getall())

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

    @defer.inlineCallbacks
    def crawl():
        runner = CrawlerRunner(get_project_settings())
        yield runner.crawl(Spider, keywords="Computer Science", location="Singapore", number=100, results=results)
        reactor.stop()

    crawl()
    reactor.run()

    with open("../../posts.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
