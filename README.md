# Web Scraper

A Python-based web crawler that scrapes and analyzes websites by making HTTP requests and parsing HTML. Generates SEO-friendly reports that can be exported to standard output or files, making it a practical tool for SEO audits, website analysis, and data extraction.

## Project Structure

* `main.py`: The main entry point for the application.
* `crawl.py`: Contains the core scraping and crawling logic.
* `async_crawler.py`: Implements asynchronous routines to speed up the crawling process.
* `json_report.py`: Handles the formatting and export of scraped data into JSON format.
* `test_crawl.py`: Test suite for verifying the crawler's functionality.
* `pyproject.toml` & `uv.lock`: Configuration and dependency lock files.

## Prerequisites

Ensure you have the following installed on your system:

* Python 3.8 or higher
* Git
* [uv](https://github.com/astral-sh/uv) (A fast Python package installer and resolver)

## Setup and Installation

1. **Clone the repository**
```bash
git clone https://github.com/Roshani-Udupa/web_scraper.git
```

2. **Navigate to the project directory**
```bash
cd web_scraper
```

3. **Install dependencies**
Use `uv` to sync the environment and install required packages:
```bash
uv sync
```

## Usage

You can run the web scraper using `uv`. The script accepts arguments such as the target URL, concurrency limits, and maximum pages to scrape. To start scraping the provided practice e-commerce site, run:
```bash
uv run main.py "https://learnwebscraping.dev/practice/ecommerce/" 2 20
```
Once the crawler finishes, the extracted data and SEO-friendly reports will be generated and saved (e.g., in `report.json`).

## Running Tests

To verify that the scraping logic and HTML parsing are functioning correctly, you can run the built-in unit tests using the following command:

```bash
uv run -m unittest
```