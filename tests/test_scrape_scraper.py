import pytest

from gorigori import scrape


def test_init():
    scrape.Scraper()


@pytest.fixture
def scraper_instance():
    return scrape.Scraper()


def test_scrape(scraper_instance: scrape.Scraper):
    scraper_instance.scrape()
    assert isinstance(
        scraper_instance.grammar_data[0]["examples"],
        list,
    )
