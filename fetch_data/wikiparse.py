import collections
import datetime
import logging
import re
import sys

import mwclient


WIKIPEDIA_URL = "en.wikipedia.org"
BIRTHS_SECTION = "==Births=="
DEATHS_SECTION = "==Deaths=="
BIRTH_PATTERN = re.compile(r"\*[\[ ]+([0-9]{1,4}[A-Za-z ]*)[\] ]+&ndash; (.+)")

logger = logging.getLogger(__name__)

class WikiParse(object):

    def __init__(self, wiki_username=None, wiki_password=None):
        self.site = mwclient.Site(WIKIPEDIA_URL)
        self.site.login(wiki_username, wiki_password)
        self.births = rdict()

    def run(self):
        for day in get_next_day():
            page_title = day.strftime("%B %-d")
            logging.info("Parsing contents for page '%s'", page_title)
            contents = self.get_wikipedia_page_contents(page_title)
            births_on_this_day = parse_births(contents)
            for birth_line in births_on_this_day:
                (year, person) = parse_birth(birth_line)
                self.births[year][day.month][day.day] = person

    def get_wikipedia_page_contents(self, page_title):
        """Return contents of Wikipedia page 'page_title'."""
        page = self.site.Pages[page_title]
        return page.edit(readonly=True)


def get_next_day():
    """Generator to iterate over every day of 2012."""

    this_day = datetime.date(2012, 1, 1)
    last_day = datetime.date(2012, 12, 31)
    one_day = datetime.timedelta(days=1)

    while this_day <= last_day:
        yield this_day
        this_day += one_day


def parse_birth(birth_text):
    """Parse birth line and return (year, person)."""
    result = BIRTH_PATTERN.search(birth_text)
    return result.groups()


def parse_births(contents):
    """Parse contents and return list of births."""
    start_index = contents.index(BIRTHS_SECTION) + len(BIRTHS_SECTION)
    end_index = contents.index(DEATHS_SECTION)
    birth_text = contents[start_index:end_index]
    return [b for b in birth_text.split("\n") if b.startswith("*")]


def rdict(*args, **kw):
    """Recursive Default Dictionary"""
    return collections.defaultdict(rdict, *args, **kw)


class Person(object):

    def __init__(self, name, link):
        self.name = name
        self.link = link


def main():
    w = WikiParse("gregono", sys.argv[1])
    w.run()
    return w

if __name__ == '__main__':
    main()
