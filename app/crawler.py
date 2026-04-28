from crawl4ai import AsyncWebCrawler
import asyncio
from typing import Optional


async def fetch_page_content(
    url: str, crawler: Optional[AsyncWebCrawler] = None
) -> str:
    """Extracts clean markdown from a URL using Crawl4AI."""

    async def _do_crawl(c):
        result = await c.arun(url=url)
        if result.success:
            return result.markdown
        raise Exception(f"Failed to crawl: {result.error_message}")

    try:
        if crawler:
            return await _do_crawl(crawler)

        # Try different API patterns for crawl4ai
        try:
            # Old API: with statement
            async with AsyncWebCrawler() as c:
                return await _do_crawl(c)
        except TypeError:
            try:
                # Newer API: create instance then use
                c = AsyncWebCrawler()
                return await _do_crawl(c)
            except TypeError:
                # Latest API: call as class
                c = await AsyncWebCrawler.create()
                try:
                    return await _do_crawl(c)
                finally:
                    if hasattr(c, "close"):
                        await c.close()
    except Exception as e:
        raise Exception(f"Crawl error: {str(e)}")
