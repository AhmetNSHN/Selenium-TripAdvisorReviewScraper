
# Selenium TripAdvisor Review Scrape
## Overview

The `Selenium-TripAdvisorReviewScraper` is a Python-based web scraping tool designed to extract reviews from TripAdvisor using Selenium. The project is aimed at automating the process of collecting user reviews and ratings for hotels, restaurants, and attractions listed on TripAdvisor. This tool allows users to collect large-scale review data for analysis, sentiment evaluation, or other research purposes.

This project used to collect training data for Sentitou project: https://github.com/AhmetNSHN/sentitou

Collected data: https://github.com/AhmetNSHN/Selenium-TripAdvisorReviewScraper/tree/main/Collected%20Data

## Features

- Scrapes reviews, ratings, and user information from TripAdvisor pages.
- Supports dynamic loading of content using Selenium to handle infinite scrolling.
- Extracts data such as:
  - Review title
  - Review body
  - Review date
  - Reviewer name
  - Reviewer location (if available)
  - Review ratings
- Stores extracted data in a structured format (CSV or JSON).
- Configurable scraping options for specific locations or businesses.

## Requirements

Before running the scraper, make sure you have the following libraries and tools installed:

- Python 3.7+
- [Selenium](https://pypi.org/project/selenium/)
- [Chrome WebDriver](https://sites.google.com/chromium.org/driver/)
- pandas
- time
- os

Install the necessary dependencies using:

```bash
pip install selenium pandas
```

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AhmetNSHN/Selenium-TripAdvisorReviewScraper.git
   cd Selenium-TripAdvisorReviewScraper
   ```

2. **Download Chrome WebDriver:**

   Make sure you have the appropriate version of the Chrome WebDriver for your Chrome browser. Place the `chromedriver` executable in your project directory or in a directory included in your system’s PATH.

   [Download Chrome WebDriver](https://sites.google.com/chromium.org/driver/)

3. **Run the Script:**

   Modify the `config.py` file to specify the URL of the TripAdvisor page you want to scrape, or pass it as a parameter to the main script.

   ```bash
   python tripadvisor_scraper.py
   ```

## Usage

### Command-Line Options

You can specify several options when running the script:

- `--url`: The TripAdvisor page URL to scrape.
- `--pages`: Number of pages to scrape.
- `--output`: Output file format (`CSV` or `JSON`).

Example:

```bash
python tripadvisor_scraper.py --url "https://www.tripadvisor.com/Hotel_Review-g12345-d1234567" --pages 5 --output reviews.csv
```

### Sample Output

The script will create an output file (`reviews.csv` or `reviews.json`) with the following structure:

| Reviewer | Review Title | Review Body | Date       | Rating | Location       |
|----------|--------------|-------------|------------|--------|----------------|
| JohnDoe  | Great Stay!  | Loved the...| 2024-09-20 | 5/5    | New York, USA  |
