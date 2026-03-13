from bs4 import BeautifulSoup

class Description:

    def __init__(self, html_doc):
        soup = BeautifulSoup(html_doc, "html.parser")
        self._text = soup.select_one("div.description__text").prettify()
        self._criteria = Criteria(soup.select_one("ul.description__job-criteria-list"))
        self._process_criteria()
        self._info = {
            "text": self._text,
            "seniority": self._seniority,
            "type": self._type,
            "function": self._function,
            "industries": self._industries
        }

    def _process_criteria(self):
        _dict = self._criteria.get_dict()
        self._seniority = _dict["Seniority level"]
        self._type = _dict["Employment type"]
        self._function = _dict["Job function"]
        self._industries = _dict["Industries"]

    def __str__(self):
        return str(self._info)

    def get_text(self):
        return self._text

class Criteria:

    def __init__(self, soup):
        keys = list(key.string.strip() for key in soup.find_all("h3", class_="description__job-criteria-subheader"))
        values = list(value.string.strip() for value in soup.find_all("span", class_="description__job-criteria-text"))
        self._dict = dict(zip(keys, values))

    def get_dict(self):
        return self._dict

if __name__ == "__main__":
    import os
    import json

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open("scraper/descriptions.json", "r", encoding="utf-8") as f:
        list(map(print, map(Description, json.load(f))))
