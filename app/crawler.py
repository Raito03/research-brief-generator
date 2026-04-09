from crawl4ai import AsyncWebCrawler
import asyncio
from typing import Optional


async def fetch_page_content(
    url: str, crawler: Optional[AsyncWebCrawler] = None
) -> str:
    """Extracts clean markdown from a URL using Crawl4AI."""

    async def _do_crawl(c: AsyncWebCrawler):
        result = await c.arun(url=url)
        if result.success:
            return result.markdown
        raise Exception(f"Failed to crawl: {result.error_message}")

    try:
        if crawler:
            return await _do_crawl(crawler)

        async with AsyncWebCrawler(verbose=False) as c:
            return await _do_crawl(c)

    except Exception as e:
        raise Exception(f"Crawl error: {str(e)}")
