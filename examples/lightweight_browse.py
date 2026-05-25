"""Minimal lightweight Webwright browsing example.

Run:
    python examples/lightweight_browse.py https://example.com
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def browse(url: str) -> None:
    workspace = Path('.tmp/webwright/example-lightweight')
    screenshots = workspace / 'screenshots'
    screenshots.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()
        await page.goto(url, wait_until='domcontentloaded')
        await page.screenshot(path=str(screenshots / 'explore_1_start.png'))
        anchors = await page.locator('a').evaluate_all("""
            els => els.slice(0, 100).map(a => ({
                text: (a.innerText || '').trim(),
                href: a.href
            }))
        """)
        print('URL:', page.url)
        print('TITLE:', await page.title())
        print(json.dumps({'top_anchors': anchors[:25]}, indent=2))
        await browser.close()


if __name__ == '__main__':
    asyncio.run(browse(sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'))
