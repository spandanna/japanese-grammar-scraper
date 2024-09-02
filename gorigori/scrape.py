"""Module for scraping example sentences for Japanese grammar points from the internet."""

import json
import time
from importlib.resources import files
from typing import List

import tqdm
from requests_cache import CachedSession

from gorigori import _constants
from gorigori._source import Source


class Scraper:
    """Class for scraping example sentences for Japanese grammar points from the internet.

    Attributes:
        session (CachedSession): Cached requests session that indefinitely stores the web scraping
            response data. This is a simple cache that uses a sqlite database in the local filesystem.
        input_fp (str): Path to a json file containing a list of grammar point dictionaries.
        grammar_database (List[dict]): The grammar data which is used to scrape examples and is populated
            with example sentences. This begins as the contents of ``input_fp`` and will be updated after each
            call to ``scrape``.

    """

    def __init__(self, input_fp: str = None):
        """Create an instance of the ``Scraper`` class.

        Args:
            input_fp (str, optional): Path to a json file containing a list of grammar point dictionaries.
                Each grammar point must have the following keys:

                    "locations" is a list of urls where the grammar point data can be scraped from
                    "examples" is a list where example sentences will be stored. It can be empty or not.

                Other keys can be present but are not required for scraping.
                Defaults to None which uses 'input.json' in the gorigori data module.

        Examples:

            Simple usage::

                from gorigori import Scraper

                scraper = Scraper()
                scraper.scrape()
                scraper.write()

            Initialise with custom input and output files::

                from gorigori import Scraper

                scraper = Scraper(input_fp="input.json")
                scraper.scrape()
                scraper.write(output_fp="output.json")

        """
        self.session = CachedSession("gorigori_cache")

        self.input_fp = input_fp or str(files(_constants.DATA_MODULE).joinpath("input.json"))

        self.grammar_data: List[dict] = self._read_input()

    def scrape(self) -> None:
        """Populate ``self.grammar_data`` with example sentences scraped from sources.

        Loops through all grammar points in the database, and parses example sentences for
        each source available for a grammar point.

        Populates the 'examples' key for each grammar point in self.grammar database.
        """
        self.prev_request_from_cache = True
        for grammar_point in tqdm.tqdm(self.grammar_data):
            for url in grammar_point.get("locations"):
                source = Source.from_location_url(url)
                if not self.prev_request_from_cache:
                    time.sleep(1)
                response = self.session.get(url)
                self.prev_request_from_cache = response.from_cache

                example_sentences = source.parse_example_sentences(response.content)

                for sentence in example_sentences:
                    if sentence not in grammar_point["examples"]:
                        grammar_point["examples"].append(sentence)

    def _read_input(self) -> List[dict]:
        """Read grammar data from ``self.input_fp``.

        Reads the input json file.

        Returns:
            List[dict]: A list of grammar points. Each grammar point is a dictionary.
        """
        with open(self.input_fp, "r") as f:
            return json.loads(f.read())

    def write(self, output_fp: str = None) -> None:
        """Write out the grammar data.

        Write current grammar data to a json file.

        Sorts the list of grammar point dictionaries alphabetically using the "romaji" key of the dictionary.
        Sorts each dictionary alphabetically.

        Args:
            output_fp (str, optional): Path to a json file where the grammar point with examples will be written to.
                Defaults to None which uses 'output.json' in the gorigori data module.
        """
        output_fp = output_fp or str(files(_constants.DATA_MODULE).joinpath("output.json"))
        grammar_data = sorted(
            self.grammar_data,
            key=lambda x: x["romaji"],
        )
        with open(output_fp, "w") as f:
            f.write(
                json.dumps(
                    grammar_data,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )
            )


if __name__ == "__main__":
    s = Scraper()
    s.scrape()
    s.write()
