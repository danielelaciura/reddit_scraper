import asyncio
import argparse
import logging
import json 
import time 
import os
from typing import List
from playwright.async_api import async_playwright, Playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#constants
REDDIT_URL = "https://www.reddit.com"

class RedditScraper:
    def __init__(self, search_query: str):
        self.search_query = search_query
        self.subreddits: List[dict] = []

    async def start_playwright(self, playwright: Playwright):
        self.playwright = playwright
        self.browser = await playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()

    async def search_subreddits(self, playwright: Playwright) -> List[dict]:
        await self.start_playwright(playwright)
        await self.page.goto(f"{REDDIT_URL}/search/?q={self.search_query}", wait_until='networkidle')
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
            
        self.page.close()

        return self.subreddits

    async def scrape_subreddit(self, subreddits, playwright: Playwright):
        try: 
            results = []
            await self.start_playwright(playwright)
            for subreddit in subreddits:
                await self.page.goto(subreddit["url"], wait_until="load", timeout=0)
                await self.page.reload()
                await self.page.mouse.wheel(0, 15000)

                try:
                    await self.page.wait_for_selector("shreddit-post-text-body p", timeout=2000)
                except:
                    pass

                try:
                    await self.page.wait_for_selector("shreddit-comment-tree p", timeout=2000)
                except:
                    pass

                body = await self.page.locator("shreddit-post-text-body p").all_text_contents()
                body_text = "\n".join(body)

                comments = await self.page.locator("shreddit-comment-tree p").all_text_contents()
                comments_text = "\n".join(comments)

                subreddit_data ={
                    "url" : subreddit["url"],
                    "title": subreddit["title"] if subreddit["title"] else "No title",
                    "scraped_at" : time.strftime("%Y-%m-%d %H:%M:%S"),
                    "body": body_text,
                    "comments_tree": comments_text
                }

                results.append(subreddit_data)
 
        except Exception as e:
            print(f'ERROR: {e}')
        
        return results

    def save_scraped_data(self, data):
        if not data:
            print("No data")
            return

        os.makedirs("data", exist_ok=True)

        filename = (
            time.strftime("%Y-%m-%d %H:%M:%S") + "_" + self.search_query + ".json"
        ).replace(" ", "_")

        filepath = os.path.join("data", filename)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=True)
            print(f"Topics saved: {filepath}")
        except Exception as e:
            print("ERROR:", e)


    async def run(self) -> List[str]:
        results = []
        async with async_playwright() as playwright:
            await self.search_subreddits(playwright)
            results = await self.scrape_subreddit(self.subreddits, playwright)
            self.save_scraped_data(results)
      
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