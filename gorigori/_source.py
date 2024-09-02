"""Internal module for configuring sources that example sentences can be pulled from."""

from abc import ABC, abstractmethod
from typing import List, Literal

from bs4 import BeautifulSoup


class Source(ABC):
    """Represents the source that example sentences are scraped from.

    Attributes:
    ----------
        base_url (Literal["https://nihongokyoshi-net.com", "https://jlptsensei.com"]): The root url for the website.

    """

    def __init__(
        self,
        base_url: Literal[
            "https://nihongokyoshi-net.com",
            "https://jlptsensei.com",
        ],
    ):
        self.base_url = base_url

    @abstractmethod
    def parse_example_sentences(
        content: bytes,
    ) -> List[str]:
        """Static, abstract method to be implemented by children.

        Parse a list of example Japanese sentences from response content bytes.

        Args:
        ----
            content (bytes): Raw bytes returned from a GET request to a single grammar point page.

        Returns:
        -------
            List[str]: Example sentences for a grammar point.

        """
        return []

    @classmethod
    def from_location_url(cls, url: str):
        if "nihongokyoshi-net" in url:
            return NihongoKyoshi()
        elif "jlptsensei" in url:
            return JLPTSensei()
        else:
            raise KeyError(f"Url not recognised. Url {url} must contain either 'nihongokyoshi-net' or 'jlptsensei'.")


class NihongoKyoshi(Source):
    """Source for scraping example sentences from https://nihongokyoshi-net.com."""

    def __init__(
        self,
        base_url: str = "https://nihongokyoshi-net.com",
    ):
        super().__init__(base_url)

    @staticmethod
    def parse_example_sentences(
        content: bytes,
    ) -> List[str]:
        """Parse a list of example Japanese sentences from response content bytes.

        Parses sentences from the html code as follows:

            - Finds all content under the '例文' ('example') header
            - Collect all paragraph items containing mostly japanese characters
            - Stops collecting when it reaches the next secondary header

        Args:
        ----
            content (bytes): Raw bytes returned from a GET request to a single grammar point page.

        Returns:
        -------
            List[str]: Example sentences for a grammar point.

        """
        example_sentences = []
        soup = BeautifulSoup(content, "html.parser")
        target = soup.find("h2", string="例文")
        for sib in target.find_all_next():
            if sib.name == "h2":
                break
            elif sib.name == "p" and len(sib.text) > 6:
                # filter out the bullet point if it exists
                text = sib.text if not sib.text.startswith("・") else sib.text[1:]
                # filtering out english examples
                text_mostly_nonascii = sum([char.isascii() for char in text]) / len(text) < 0.5
                if text_mostly_nonascii:
                    example_sentences.append(text)
        return example_sentences


class JLPTSensei(Source):
    """Source for scraping example sentences from https://jlptsensei.com."""

    def __init__(
        self,
        base_url: str = "https://jlptsensei.com",
    ):
        super().__init__(base_url)

    @staticmethod
    def parse_example_sentences(
        content: bytes,
    ) -> List[str]:
        """Parse a list of example Japanese sentences from response content bytes.

        Parses sentences from the html code as follows:

            - Collects all paragraph items on the page with the 'm-o' and 'jp' attributes

        Args:
        ----
            content (bytes): Raw bytes returned from a GET request to a single grammar point page.

        Returns:
        -------
            List[str]: Example sentences for a grammar point.

        """
        example_sentences = []
        soup = BeautifulSoup(content, "html.parser")
        target = soup.find_all(name="p", attrs=["m-0", "jp"])
        for sentence in target:
            example_sentences.append(sentence.text)
        return example_sentences
