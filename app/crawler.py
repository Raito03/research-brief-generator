from crawl4ai import AsyncWebCrawler
import asyncio


async def fetch_page_content(url: str) -> str:
    """Extracts clean markdown from a URL using Crawl4AI."""
    try:
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=url)
            if result.success:
                return result.markdown
            return f"Failed to crawl: {result.error_message}"
    except Exception as e:
        return f"Crawl error: {str(e)}"
