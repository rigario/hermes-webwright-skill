"""Final Webwright script skeleton.

Copy into `.tmp/webwright/<slug>/final_runs/run_1/final_script.py` and adapt.
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

RUN_DIR = Path(__file__).parent
SCREENSHOTS = RUN_DIR / 'screenshots'
LOG = RUN_DIR / 'final_script_log.txt'
RESULT = RUN_DIR / 'result.json'


def log(step: int, message: str) -> None:
    line = f"step {step} action: {message}"
    print(line)
    with LOG.open('a') as f:
        f.write(line + '
')


async def main() -> None:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    LOG.write_text('')

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()

        step = 1
        await page.goto('https://example.com', wait_until='domcontentloaded')
        log(step, f'opened page: {page.url}')
        await page.screenshot(path=str(SCREENSHOTS / 'final_execution_1_open_page.png'))

        title = await page.title()
        assert title, 'expected non-empty page title'
        RESULT.write_text(json.dumps({'url': page.url, 'title': title}, indent=2))
        log(step + 1, f'FINAL_RESPONSE: {title}')
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
