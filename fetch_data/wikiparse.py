"""wikiparse.py

A script for fetching all birthday information from Wikipedia and saving it to
a JSON object.
"""


import collections
import datetime
import logging
from optparse import OptionParser
import re

import mwclient


WIKIPEDIA_URL = "en.wikipedia.org"
BIRTHS_SECTION = "==Births=="
DEATHS_SECTION = "==Deaths=="


# Regular Expression Patterns
# Extract birth year from rest of birth line information.
# Year may include optional era, like "BC".
YEAR_PAT = re.compile(r"\*[\[ ]+(?P<year>[0-9]{1,4}[A-Za-z ]*)[\] ]+&ndash; (?P<person_info>.+)")


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
    result = YEAR_PAT.search(birth_text)
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


def parse_command_line_options():
    """Parse and return command line options."""
    parser = OptionParser()
    parser.add_option("--username", help="Username for Wikipedia account")
    parser.add_option("--password", help="Password for Wikipedia account")
    parser.add_option("-q", action="store_false", dest="verbose", default=True,
                      help="Don't print info messages to stdout")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments")
    return options


def main():
    options = parse_command_line_options()
    w = WikiParse(options.username, options.password)
    w.run()
    return w


if __name__ == '__main__':
    main()
