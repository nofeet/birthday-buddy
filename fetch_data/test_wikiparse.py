# Test module for wikiparse
# -*- coding: utf-8 -*-

import unittest

import wikiparse


# Condensed example content for a Wikipedia day page.
WIKI_DAY_CONTENT = """
{{pp-move-indef}}{{JanuaryCalendar|float=right}}
{{ThisDateInRecentYears}}
{{Day}} The [[Perihelion]], the point in the year when the Earth is closest to the Sun, occurs around this date.

==Events==
*[[1431]] &ndash; [[Joan of Arc]] is handed over to [[Roman Catholic Diocese of Beauvais|Bishop]] [[Pierre Cauchon]].
*[[1496]] &ndash; [[Leonardo da Vinci]] unsuccessfully tests a flying machine.
*[[1999]] &ndash; The ''[[Mars Polar Lander]]'' is launched.
*  1999   &ndash; [[Israel]] detains, and later expels, 14 members of [[Concerned Christians]].
*[[2004]] &ndash; [[Flash Airlines Flight 604]] crashes into the [[Red Sea]], resulting in 148 deaths, making it the deadliest aviation accident in Egyptian history.

==Births==
<!-- Please do not add yourself or anyone else without a biography in Wikipedia to this list.-->
*[[106 BC]] &ndash; [[Cicero]], Roman statesman and philosopher (d. 43 BC)
*[[1196]] &ndash; [[Emperor Tsuchimikado]] of Japan (d. 1231)
*[[1698]] &ndash; [[Pietro Metastasio]], Italian poet (d. 1782)
*[[1862]] &ndash; [[Matthew Nathan|Sir Matthew Nathan]], British Governor of [[Queensland]] (d. 1939)
*[[1865]] &ndash; [[Henry Lytton]], British actor and opera singer (d. 1936)
*[[1876]] &ndash; [[Wilhelm Pieck]], East Germany statesman (d. 1960)
*[[1879]] &ndash; [[Grace Coolidge]], [[First Lady of the United States]] (d. 1957)
*[[1883]] &ndash; [[Clement Attlee]], [[Prime Minister of the United Kingdom]] (d. 1967)
*[[1884]] &ndash; [[Raoul von Koczalski]], Polish pianist and composer (d. 1948)
*[[1885]] &ndash; [[Harry Elkins Widener]], American book collector and victim of the [[RMS Titanic]] sinking (d. 1912
*[[1989]] &ndash; [[Alex D. Linz]], American actor
*  1989   &ndash; [[Julia Nunes]], American singer and ukulele player
*1989 &ndash; [[Anya Rozova]], Russian/American fashion model
*[[1991]] &ndash; [[Jerson Cabral]], Dutch footballer
<!-- 
Please do not add yourself, non-notable people, fictional characters, or people without Wikipedia articles to this list. No red links, please. 
Do not link multiple occurrences of the same year, just link the first occurrence.
If there are multiple people in the same birth year, put them in alphabetical order.
Do not trust "this year in history" websites for accurate date information. -->

==Deaths==
* [[235]] &ndash; [[Pope]] St. [[Anterus]]
* [[323]] &ndash; [[Emperor Yuan of Jin|Jin Yuandi]], Chinese emperor of the [[Jin Dynasty (265-420)|Jin Dynasty]] (b. 276)
*[[1098]] &ndash; [[Walkelin]], Norman [[bishop of Winchester]]
*[[2011]] &ndash; [[Fadil Hadžić]], Croatian film director (b. 1922)
*  2012   &ndash; [[Willi Entenmann]], German footballer and footballcoach (b. 1943)
*[[2012]] &ndash; [[Josef Škvorecký]], Czech writer and publisher (b. 1924)
*[[2012]] &ndash; [[Gatewood Galbraith]], American politician (b. 1947)
*  2012   &ndash; [[Bob Weston (guitarist)|Bob Weston]], British musician (b. 1947)
<!--
Do not add people without Wikipedia articles to this list
Do not trust “this year in history” websites for accurate date information
Do not link multiple occurrences of the same year, just link the first occurrence.
-->

==Holidays and observances==
*Christian [[Feast Day]]:
**[[Genevieve]]
**[[January 3 (Eastern Orthodox liturgics)]]

*[[Hakozaki_Shrine#Festivals|Tamaseseri Festival]] ([[Hakozaki Shrine]], [[Fukuoka]])
*The tenth [[twelvetide|day of Christmas]] ([[Western Christianity]])

==External links==
{{commons}}
* [http://news.bbc.co.uk/onthisday/hi/dates/stories/january/3 BBC: On This Day]
* {{NYT On this day|month=01|day=03}}
* [http://www1.sympatico.ca/cgi-bin/on_this_day?mth=Jan&day=03 On This Day in Canada]
----
{{months}}

{{DEFAULTSORT:January 03}}
[[Category:Days of the year]]
[[Category:January]]

[[af:3 Januarie]]
[[zea:3 januari]]
"""

EXPECTED_BIRTHS = [
    '*[[106 BC]] &ndash; [[Cicero]], Roman statesman and philosopher (d. 43 BC)',
    '*[[1196]] &ndash; [[Emperor Tsuchimikado]] of Japan (d. 1231)',
    '*[[1698]] &ndash; [[Pietro Metastasio]], Italian poet (d. 1782)',
    '*[[1862]] &ndash; [[Matthew Nathan|Sir Matthew Nathan]], British Governor of [[Queensland]] (d. 1939)',
    '*[[1865]] &ndash; [[Henry Lytton]], British actor and opera singer (d. 1936)',
    '*[[1876]] &ndash; [[Wilhelm Pieck]], East Germany statesman (d. 1960)',
    '*[[1879]] &ndash; [[Grace Coolidge]], [[First Lady of the United States]] (d. 1957)',
    '*[[1883]] &ndash; [[Clement Attlee]], [[Prime Minister of the United Kingdom]] (d. 1967)',
    '*[[1884]] &ndash; [[Raoul von Koczalski]], Polish pianist and composer (d. 1948)',
    '*[[1885]] &ndash; [[Harry Elkins Widener]], American book collector and victim of the [[RMS Titanic]] sinking (d. 1912',
    '*[[1989]] &ndash; [[Alex D. Linz]], American actor',
    '*  1989   &ndash; [[Julia Nunes]], American singer and ukulele player',
    '*1989 &ndash; [[Anya Rozova]], Russian/American fashion model',
    '*[[1991]] &ndash; [[Jerson Cabral]], Dutch footballer'
]


class TestWikiParse(unittest.TestCase):

    longMessage = True

    def test_get_next_day(self):
        "Verify get_next_day() returns every day of (leap) year."""
        days = list(wikiparse.get_next_day())
        self.assertEqual(366, len(days), "Wrong number of days returned.")

    def test_parse_birth_ad(self):
        """Verify that parse_birth() parses a single AD Birth line correctly."""
        birth_line = "*[[1862]] &ndash; [[Matthew Nathan|Sir Matthew Nathan]], British Governor of [[Queensland]] (d. 1939)"
        (actual_year, actual_name) = wikiparse.parse_birth(birth_line)
        self.assertEqual("1862", actual_year, "Wrong year returned")
        self.assertEqual("[[Matthew Nathan|Sir Matthew Nathan]], British Governor of [[Queensland]] (d. 1939)", actual_name, "Wrong name returned")

    def test_parse_birth_bc(self):
        """Verify that parse_birth() parses a single BC Birth line correctly."""
        birth_line = "*[[106 BC]] &ndash; [[Cicero]], Roman statesman and philosopher (d. 43 BC)"
        (actual_year, actual_name) = wikiparse.parse_birth(birth_line)
        self.assertEqual("106 BC", actual_year, "Wrong year returned")
        self.assertEqual("[[Cicero]], Roman statesman and philosopher (d. 43 BC)", actual_name, "Wrong name returned")

    def test_parse_births(self):
        """Verify parse_births() returns all birth entries and nothing else."""
        actual_births = wikiparse.parse_births(WIKI_DAY_CONTENT)
        self.assertListEqual(EXPECTED_BIRTHS, actual_births)
