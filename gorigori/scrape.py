import datetime as dt
import json
import os
import time

from requests_cache import CachedSession

from gorigori.source import Source


class Scraper:
    def __init__(self):
        self.session = CachedSession("japanese_grammar_cache")
        self.prev_request_from_cache = True
        self.data_dir = "data"
        self.input_file = os.path.join(self.data_dir, "input.json")
        self.output_file = os.path.join(self.data_dir, "output.json")

        self.grammar_database = self.read()

    def scrape_example_sentences(self) -> None:
        """Populate self.grammar_database with freshly scraped example sentences."""
        for grammar_point in self.grammar_database:
            for url in grammar_point.get("locations"):
                source = Source.from_location_url(url)
                if not self.prev_request_from_cache:
                    time.sleep(1)
                response = self.session.get(url)
                self.prev_request_from_cache = response.from_cache

                example_sentences = source.parse_example_sentences(response.content)
                grammar_point["examples"] += list(example_sentences)

    def read(self) -> str:
        with open(self.input_file, "r") as f:
            return json.loads(f.read())

    def write(self) -> None:
        with open(self.output_file, "w") as f:
            f.write(json.dumps(self.grammar_database, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    s = Scraper()
    s.scrape_example_sentences()
    s.write()
