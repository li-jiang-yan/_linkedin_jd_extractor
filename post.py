import os
import json
from bs4 import BeautifulSoup

class Post:

    def __init__(self, html_doc):
        soup = BeautifulSoup(html_doc, "html.parser")
        self._title = soup.select_one("a.base-card__full-link").span.string.strip()
        self._link = soup.select_one("a.base-card__full-link").get("href")
        self._company = Company(soup.select_one("h4.base-search-card__subtitle"))
        self._location = soup.select_one("span.job-search-card__location").string.strip()
        self._listdate = soup.time.get("datetime")
        self._info = {
            "title": self._title,
            "link": self._link,
            "company.name": self._company._name,
            "company.link": self._company._link,
            "location": self._location,
            "listdate": self._listdate
        }

    def __str__(self):
        return str(self._info)

class Company:

    def __init__(self, soup):
        self._name = soup.a.string.strip()
        self._link = soup.select_one("a.hidden-nested-link").get("href")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open("scraper/posts.json", "r", encoding="utf-8") as f:
        list(map(print, map(Post, json.load(f))))
