from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class Source(ABC):
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
        else:
            raise KeyError("url not recognised.")


class NihongoKyoshi(Source):
    def __init__(self, base_url: str = "https://nihongokyoshi-net.com"):
        super().__init__(base_url)

    @staticmethod
    def parse_example_sentences(content: bytes) -> list:
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
        example_sentences = []
        soup = BeautifulSoup(content, "html.parser")
        target = soup.find_all(name="p", attrs=["m-0", "jp"])
        for sentence in target:
            example_sentences.append(sentence.text)
        return example_sentences

    @staticmethod
    def format_example_sentence(string: str) -> str:
        return string[1:]
