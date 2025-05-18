# CAB Meeting Minutes Scraper

## Objective

Build a web scraper using the **Python Scrapy framework** to extract specific document URLs and metadata from the **Colorado Department of Transportation CAB Meeting Minutes** webpage.

---

## Project Overview

This Scrapy project is designed to crawl the first **two pages** of the CAB Meeting Minutes table and extract relevant details about each document, including:

- Meeting date (in `yyyy-mm-dd` format)
- Meeting title
- Document category (`minutes` or `other`)
- Document URL

The extracted data is saved into a structured CSV file.

---

## Features

- **Multi-page scraping:** Extract data from the first 2 pages of the meeting minutes.
- **Date normalization:** Dates are parsed and formatted as `yyyy-mm-dd`.
- **Category assignment:** Documents are classified as either `minutes` or `other`.
- **CSV output:** Saves data in a CSV file with specified columns.
- **Easy to run:** Runs with the standard Scrapy command line interface.

---

## Requirements

- Python 3.x
- Scrapy framework (`pip install scrapy`)

---

## Installation & Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Navigate into the project directory:
    ```bash
    cd cab_minutes_scraper
    ```
3. Install Scrapy if not already installed:
    ```bash
    pip install scrapy
    ```

---

## Usage

Run the spider using the following command:

```bash
scrapy crawl cab -o cab_meetings.csv
