"""
Reddit Scraper - Main Application
A web scraper that searches Reddit and extracts data from subreddit pages.

Project Structure:
    reddit_scraper/
    ├── main.py              # This file - main application
    ├── requirements.txt     # Python dependencies
    ├── README.md           # Project documentation
    └── .gitignore          # Git ignore file

Installation:
    pip install -r requirements.txt
    playwright install      # Install browser binaries

Usage:
    python main.py "python programming"
    python main.py --interactive
"""

import asyncio
from typing import List, Optional
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RedditScraper:
    """Main scraper class that coordinates search and data extraction."""
    
    def __init__(self, search_query: str):
        """
        Initialize the Reddit scraper.
        
        Args:
            search_query: The search term to use on Reddit
        """
        self.search_query = search_query
        self.subreddits: List[str] = []
        
    async def search_subreddits(self) -> List[str]:
        """
        Search Reddit for subreddits matching the query using Playwright.
        
        Returns:
            List of subreddit names found
        """
        logger.info(f"Searching Reddit for: {self.search_query}")
        
        # TODO: Implement Playwright-based Reddit search
        # This should:
        # 1. Launch browser with Playwright
        # 2. Navigate to Reddit search
        # 3. Enter search query
        # 4. Extract subreddit names from results
        # 5. Return list of subreddit names
        
        raise NotImplementedError("Playwright search not yet implemented")
    
    async def scrape_subreddit(self, subreddit_name: str) -> dict:
        """
        Scrape a single subreddit page using Playwright and BeautifulSoup.
        
        Args:
            subreddit_name: Name of the subreddit to scrape
            
        Returns:
            Dictionary containing scraped data
        """
        logger.info(f"Scraping subreddit: r/{subreddit_name}")
        
        # TODO: Implement subreddit scraping
        # This should:
        # 1. Use Playwright to navigate to subreddit
        # 2. Get the page HTML
        # 3. Parse HTML with BeautifulSoup
        # 4. Extract relevant data
        # 5. Return structured data
        
        raise NotImplementedError("Subreddit scraping not yet implemented")
    
    async def run(self) -> dict:
        """
        Execute the full scraping workflow.
        
        Returns:
            Dictionary containing all scraped data
        """
        try:
            # Step 1: Search for subreddits
            self.subreddits = await self.search_subreddits()
            logger.info(f"Found {len(self.subreddits)} subreddits")
            
            # Step 2: Scrape each subreddit
            results = {}
            for subreddit in self.subreddits:
                try:
                    data = await self.scrape_subreddit(subreddit)
                    results[subreddit] = data
                except Exception as e:
                    logger.error(f"Error scraping r/{subreddit}: {e}")
                    results[subreddit] = {"error": str(e)}
            
            return results
            
        except Exception as e:
            logger.error(f"Scraping workflow failed: {e}")
            raise


def get_search_query() -> str:
    """
    Collect search query from user input.
    
    Returns:
        Search query string
    """
    parser = argparse.ArgumentParser(
        description='Reddit Scraper - Search and extract data from Reddit'
    )
    parser.add_argument(
        'query',
        type=str,
        nargs='?',
        help='Search query for Reddit'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # Get query from command line or prompt user
    if args.query:
        return args.query
    elif args.interactive or not args.query:
        query = input("Enter your Reddit search query: ").strip()
        if not query:
            raise ValueError("Search query cannot be empty")
        return query
    else:
        parser.print_help()
        raise ValueError("No search query provided")


async def main():
    """Main entry point for the application."""
    try:
        # Get search query from user
        search_query = get_search_query()
        logger.info(f"Starting Reddit scraper with query: '{search_query}'")
        
        # Initialize and run scraper
        scraper = RedditScraper(search_query)
        results = await scraper.run()
        
        # Display results
        logger.info("Scraping completed successfully")
        print("\n=== Results ===")
        for subreddit, data in results.items():
            print(f"\nr/{subreddit}:")
            print(f"  {data}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())