# Japanese grammar scraper

A web scraping project to pull example sentences for japanese grammar points. This is useful when wanting to learn grammar points by context rather than by definition. This project creates a package `gorigori` which can be used to scrape example sentences and a simple API which can be used to retrieve the scraped data.

# To run

*Note: This project has been created and tested using python 3.12.*

## Scraper

Create a virtual environment and install gorigori as a package with dev requirements:

    pip install -e '.[dev]'

Scrape all the example sentences for the inputted grammar points using: 

    python -m gorigori.scrape

Or import and use the package as follows:

    from gorigori import Scraper

    scraper = Scraper()
    scraper.scrape()
    scraper.write()

## API

A simple API has been made to retrieve generated grammar points.

To run the API locally use:

    uvicorn api.main:app --reload

# Tests

Tests have been created using `pytest`. You can run them using: 

    pytest tests

# Docs

Docs are built using `sphinx`.

Install the docs requirements:

    pip install -e '.[docs]'

To rebuild the docs run the following command from the `docs` directory:

    make html


# Notes

To avoid exceeding rate-limiting thresholds all new requests are delayed by 1 second. All requests are cached indefinitely.


