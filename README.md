![Tests](https://github.com/spandanna/japanese-grammar-scraper/actions/workflows/test.yml/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img src="./docs/source/_static/logo.png" width="200" height="200" />

# Japanese grammar scraper

A web scraping project to pull example sentences for Japanese grammar points! This is useful if you want to learn grammar by context rather than by trying to learn the definition or rule. 

This project consist of a package `gorigori` which can be used to scrape example sentences and a simple API which can be used to retrieve the scraped data.


# How to use

*Note: This project only supports python >=3.10*

## Scraper

Create a virtual environment and install `gorigori` from the repo as a package:

    pip install -e .

Scrape all the example sentences for the inputted grammar points using: 

    python -m gorigori.scrape

Or import and use the package in a script as follows:

    from gorigori import Scraper

    scraper = Scraper()
    scraper.scrape()
    scraper.write()

## API

A simple API has been made to retrieve generated grammar points.

Install API requirements:

    pip install -r requirements.txt

Run the API:

    uvicorn api.main:app --reload

# Tests

Tests have been created for `gorigori` using `pytest`. 

Install the test requirements:

    pip install -e '.[test]'

Run tests:

    pytest tests

# Docs

Docs are built using `sphinx`.

Install the docs requirements:

    pip install -e '.[docs]'

Build the docs:

    cd docs
    make html


# Notes

To avoid exceeding rate-limiting thresholds all new requests are delayed by 1 second. All requests are cached indefinitely.


