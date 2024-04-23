import datetime as dt
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from requests_cache import CachedSession


class Source(ABC):
    """Represents the source that example sentences are scraped from."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def parse_example_sentences(content: bytes) -> list:
        pass

    def format_example_sentence(string: str) -> str:
        pass

    @classmethod
    def from_location_url(cls, url: str):
        if "nihongokyoshi-net" in url:
            return NihongoKyoshi()
        elif "jlptsensei" in url:
            return JLPTSensei()
        elif "google" in url:
            return GoogleNews()
        else:
            raise KeyError("url not recognised.")


class NihongoKyoshi(Source):
    def __init__(self, base_url: str = "https://nihongokyoshi-net.com"):
        super().__init__(base_url)

    @staticmethod
    def parse_example_sentences(content: bytes) -> list:
        """Parses example japanese sentences from the html source code.

        - Finds all content under the '例文' header
        - Collect all paragraph items that contain japanese characters
        - Stops collecting when it reaches the next secondary header
        """
        example_sentences = []
        soup = BeautifulSoup(content, "html.parser")
        target = soup.find("h2", string="例文")
        for sib in target.find_all_next():
            if sib.name == "h2":
                break
            elif sib.name == "p" and not sib.text.isascii():
                example_sentences.append(sib.text)
        return example_sentences

    @staticmethod
    def format_example_sentence(string: str) -> str:
        return string[1:]


class JLPTSensei(Source):
    def __init__(self, base_url: str = "https://jlptsensei.com"):
        super().__init__(base_url)

    @staticmethod
    def parse_example_sentences(content: bytes) -> list:
        """Parses example japanese sentences from the html source code.

        - Collects all paragraph tags on the page with the 'm-o' and 'jp' attributes

        """
        example_sentences = []
        soup = BeautifulSoup(content, "html.parser")
        target = soup.find_all(name="p", attrs=["m-0", "jp"])
        for sentence in target:
            example_sentences.append(sentence.text)
        return example_sentences

    @staticmethod
    def format_example_sentence(string: str) -> str:
        return string


class GoogleNews(Source):
    def __init__(self, base_url: str = "https://www.google.com/search"):
        super().__init__(base_url)

    @staticmethod
    def parse_example_sentences(content: bytes) -> list:
        """Parses example japanese sentences from google news search results.

        Not yet implemented.
        """

        session = CachedSession(
            "japanese_grammar_cache", expire_after=dt.timedelta(days=7)
        )

        example_sentences = []

        soup = BeautifulSoup(content, "html.parser")

        # find links to hnews articles
        target = soup.find_all(name="a")
        news_articles = [title.href for title in target]

        # pull html for each article
        # do some simple regex to extract the sentence containing the target grammar

        return example_sentences

    @staticmethod
    def format_example_sentence(string: str) -> str:
        return string
