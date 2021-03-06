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
import simplejson


logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger("wikiparse")

# Constants
WIKIPEDIA_URL = "en.wikipedia.org"
MIN_YEAR = 1900

# Regular Expression Patterns
BIRTHS_SECTION_PAT = re.compile(r"== *Births *==")
DEATHS_SECTION_PAT = re.compile(r"== *Deaths *==")
# Extract birth year from rest of birth line information.
# Year may include optional era, like "BC".
YEAR_PAT = re.compile(r"\*[\[ ]*(?P<year>[0-9]{1,4}[A-Za-z ]*)[\] ]*&ndash; +(?P<person_info>.+)")


class WikiParse(object):

    def __init__(self, wiki_username=None, wiki_password=None, verbose=False):
        self.site = mwclient.Site(WIKIPEDIA_URL)
        self.site.login(wiki_username, wiki_password)
        self.births = collections.defaultdict(list)
        if verbose:
            logger.setLevel(logging.INFO)

    def fetch_data(self):
        logger.info("Starting Wikipedia parse")
        for day in get_next_day():
            page_title = day.strftime("%B %-d")
            logger.info("Parsing contents for page '%s'", page_title)
            contents = self.get_wikipedia_page_contents(page_title)
            births_on_this_day = parse_births(contents)
            for birth_line in births_on_this_day:
                (year, person) = parse_birth(birth_line)
                if not year:
                    continue
                year = year.rstrip()
                try:
                    year = int(year)
                except ValueError:
                    logger.warning("Skipping entry with bad year: " + birth_line)
                    continue
                if year > MIN_YEAR:
                    self.births["%d%s%s" % (year, day.month, day.day)].append(person)
                else:
                    logger.debug("Skipping old entry: " + birth_line)
        logger.info("Finished Wikipedia parse")

    def get_wikipedia_page_contents(self, page_title):
        """Return contents of Wikipedia page 'page_title'."""
        page = self.site.Pages[page_title]
        return page.edit(readonly=True)

    def dump_to_json_file(self, filename="birthdays.json"):
        """Serialize this object to a JSON formatted string."""
        with open(filename, 'w') as f:
            simplejson.dump(self.births, f)


def get_next_day():
    """Generator to iterate over every day of 2012."""
    this_day = datetime.date(2012, 1, 1)
    last_day = datetime.date(2012, 12, 31)
    one_day = datetime.timedelta(days=1)

    while this_day <= last_day:
        yield this_day
        this_day += one_day


def parse_birth(birth_text):
    """Parse birth line and return (year, person).

    If birth_text is unrecognizable, return empty string for year and person.
    """
    result = YEAR_PAT.search(birth_text)
    try:
        return result.groups()
    except AttributeError:
        logger.warning("Cannot parse '%s'." % birth_text)
        return ("", "")


def parse_births(contents):
    """Parse contents and return list of births."""
    contents_after_births = BIRTHS_SECTION_PAT.split(contents)[1]
    birth_text = DEATHS_SECTION_PAT.split(contents_after_births)[0]
    return [b for b in birth_text.split("\n") if b.startswith("*")]


def parse_command_line_options():
    """Parse and return command line options."""
    parser = OptionParser()
    parser.add_option("--username", help="Username for Wikipedia account")
    parser.add_option("--password", help="Password for Wikipedia account")
    parser.add_option("--verbose", action="store_true", default=False,
                      help="Print info messages to stdout")
    (options, args) = parser.parse_args()
    if args:
        parser.error("Unknown argument(s): %s" % ", ".join(args))
    return options


def main():
    options = parse_command_line_options()
    w = WikiParse(options.username, options.password, options.verbose)
    w.fetch_data()
    return w.dump_to_json_file()


if __name__ == '__main__':
    main()
