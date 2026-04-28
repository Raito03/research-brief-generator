import pytest


def test_fetch_page_content():
    """
    Test crawler module imports correctly.
    Actual crawling tested in integration/deployed environment.
    """
    # Verify module can be imported
    from app import crawler

    assert hasattr(crawler, "fetch_page_content")

    # The function is async - that's tested in integration
    assert asyncio.iscoroutinefunction(crawler.fetch_page_content) is True


import asyncio
