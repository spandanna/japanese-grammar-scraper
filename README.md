# Japanese grammar scraper
A webscraping project to pull example sentences for japanese grammar points from learning sources. This is useful when wanting to learn grammar by context rather than by definitions.

# To run
*Note: This project has been created and tested using python 3.12.*

Create a virtual environment and install requirements.

Manually populate data/input.json with data for the grammar points you are interested in. Include location urls from  sources (currently implemented JLPT Sensei or Nihongo Kyoshi).

Scrape all the example sentences for the inputted grammar points using: 

`python -m gorigori.scrape`

# Tests
Tests are created using pytest. You can run them using: 

`pytest tests`

# Notes
To avoid exceeding rate-limiting thresholds, code has been implemented to delay all new requests by 1 second. All requests are cached and expire after 1 day.


