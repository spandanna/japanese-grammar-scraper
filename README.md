# Japanese grammar dataset
A webscraping project to pull example sentences for japanese grammar points from learning sources.

# To run
Create a virtual environment and install requirements.

Manually populate data/input.json with data for the grammar points you are interested in. Include location urls from  sources (currently implemented JLPT Sensei or Nihongo Kyoshi).

Scrape all the example sentences for the inputted grammar points using: 
`python -m gorigori.scrape`

# Tests
Tests are created using pytest. You can run using: 
`pytest tests`

# Notes
Requests are cached locally to avoid exceeding rate-limiting thresholds. This includes any requests ran during testing.


