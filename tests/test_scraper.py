import pytest

import gorigori.scrape as scrape


def test_init():
    scrape.Scraper()


@pytest.fixture
def scraper_instance():
    return scrape.Scraper()


def test_scrape_example_sentences(scraper_instance):
    scraper_instance.scrape_example_sentences()
    assert isinstance(scraper_instance.grammar_database[0]["examples"], list)
