# Reddit Scraper

A Python-based web scraper that searches Reddit for subreddits and extracts data using Playwright and BeautifulSoup.

## Features

- Search Reddit for subreddits based on a query string
- Automated browser interaction using Playwright
- HTML parsing and data extraction with BeautifulSoup
- Asynchronous operation for better performance
- Command-line and interactive input modes

## Installation

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Usage

### Command-line mode:
```bash
python main.py "your search query"
```

### Interactive mode:
```bash
python main.py --interactive
```

### Examples:
```bash
python main.py "python programming"
python main.py "machine learning"
python main.py -i
```

## Project Structure

```
reddit_scraper/
├── main.py              # Main application with RedditScraper class
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore patterns
```

## Implementation Checklist

- [x] Project structure and boilerplate
- [x] Input data collection (CLI + interactive)
- [x] Dependencies setup (requirements.txt)
- [ ] Playwright Reddit search implementation
- [ ] Subreddit page scraping with Playwright
- [ ] BeautifulSoup HTML parsing
- [ ] Data extraction logic
- [ ] Error handling and retries
- [ ] Rate limiting
- [ ] Data export functionality

## Dependencies

- **Playwright**: Browser automation for navigating Reddit
- **BeautifulSoup4**: HTML parsing and data extraction
- **lxml**: Fast XML/HTML parser for BeautifulSoup
- **asyncio**: Asynchronous programming support

## Notes

- Reddit may have rate limiting and anti-scraping measures
- Consider Reddit's robots.txt and terms of service
- Use appropriate delays between requests
- Consider using Reddit's API for production use cases

## License

[Your License Here]