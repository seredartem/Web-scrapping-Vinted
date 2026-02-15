# Web-scrapping-Vinted
Python CLI Vinted scraper: parses catalog pages, saves product data &amp; images, and tracks per-page byte stats


A CLI Python project for scraping the Vinted (vinted.pl) catalog: collects product cards from search pages, saves product info into `.txt` files, downloads images, calculates per-page byte statistics, and stores parsing history.

> Educational / pet project to practice: Requests, BeautifulSoup, filesystem operations, error handling, and basic analytics.

## Features
- Scrape products from catalog/search pages (`page=1..N`)
- Extract product data:
  - Title, Link, Price, Size, Quality
  - Image URLs list
- Save results into a structured folder layout:
  - separate folder per page
  - separate folder per product
  - `.txt` file with product metadata
  - `images/` folder with downloaded images
- Calculate downloaded data size (bytes) per page
- Store parsing history in a log file

## Tech Stack
- Python 3.x
- `requests`
- `beautifulsoup4`
- Parser: `lxml`
