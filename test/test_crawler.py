import pytest
import asyncio
from app.crawler import fetch_page_content


@pytest.mark.asyncio
async def test_fetch_page_content():
    # Test a reliable, fast URL
    url = "https://example.com"
    content = await fetch_page_content(url)

    assert content is not None
    assert "Example Domain" in content
    assert len(content) > 50
