import asyncio
import argparse
import logging
import json 
import time 
from typing import List, Optional
from bs4 import BeautifulSoup 
from playwright.async_api import async_playwright, Playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#constants
REDDIT_URL = "https://www.reddit.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class RedditScraper:
    def __init__(self, search_query: str):
        self.search_query = search_query
        self.subreddits: List[dict] = []
        self.page = None
        self.browser = None
        self.playwright = None

    async def start_playwright(self, playwright: Playwright, url):
        self.playwright = playwright
        self.browser = await playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        await self.page.goto(url, wait_until='networkidle')

    async def search_subreddits(self, playwright: Playwright) -> List[dict]:
        url = f"{REDDIT_URL}/search/?q={self.search_query}"
        await self.start_playwright(playwright, url)
        await self.page.reload()

        # for i in range(20):
        #     await self.page.mouse.wheel(0, 15000)
        #     self.page.mouse.wheel(0, 15000)
        #     time.sleep(2)
        # time.sleep(15)

        posts = self.page.get_by_test_id('post-title')
        count = await posts.count()

        for i in range(count):
            post = posts.nth(i)
            title = await post.inner_text()
            href = await post.get_attribute("href")
            if href and href.startswith("/"):
                href = REDDIT_URL + href

            self.subreddits.append({"title": title, "url": href})

        return self.subreddits

    async def scrape_subreddit(self, subreddit: dict, playwright: Playwright) -> str:
        try: 
            await self.start_playwright(playwright, subreddit["url"])
            await self.page.reload()
         
            body = await self.page.locator("shreddit-post-text-body p").all_text_contents()
            text = "\n".join(body)
            subreddit_data ={
                "url" : subreddit["url"],
                "title": subreddit["title"] if subreddit["title"] else "No title",
                "scraped_at" : time.strftime("%Y-%m-%d %H:%M:%S"),
                "body": text
            }
 
        except Exception as e:
            print(f'ERROR: {e}')
        
        return subreddit_data

    def save_scraped_data(self, data):
        if not data:
            print(f'No data')
            return 
        filename_json= (self.search_query + time.strftime("%Y-%m-%d %H:%M:%S") + ".json").replace(" ", "_") 
        # JSON
        try:
            with open(filename_json, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=True)
            print(f'Python Topics saved: {filename_json}')
        except Exception as e:
            print("ERROR:",e)

    async def run(self) -> List[str]:
        async with async_playwright() as playwright:
            await self.search_subreddits(playwright)

        results = []
        for subreddit in self.subreddits:
            try:
                async with async_playwright() as playwright:
                    data = await self.scrape_subreddit(subreddit, playwright)
                results.append(data)
            except Exception as e:
                logger.error(f"Error scraping {subreddit}: {e}")
        self.save_scraped_data(results)
        # if self.browser:
        #     await self.browser.close()
        return results
        
def get_search_query() -> str:
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
    try:
        search_query = get_search_query()
        logger.info(f"Starting Reddit scraper with query: '{search_query}'")
        # Initialize and run scraper
        scraper = RedditScraper(search_query)
        await scraper.run()
                
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")

if __name__ == "__main__":
   asyncio.run(main())