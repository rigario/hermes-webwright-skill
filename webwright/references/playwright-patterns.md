# Webwright Playwright Patterns for Hermes

## Launch Skeleton

Use this pattern for scratch exploration and final scripts:

```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE = Path('.tmp/webwright/<slug>')
SCREENSHOTS = WORKSPACE / 'screenshots'
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()
        await page.goto('<START_URL>', wait_until='domcontentloaded')
        await page.screenshot(path=str(SCREENSHOTS / 'explore_1_start.png'))
        print('URL:', page.url)
        print('TITLE:', await page.title())
        print(await page.locator('body').aria_snapshot())
        await browser.close()

asyncio.run(main())
```

## Selector Preference

1. `page.get_by_role(role, name='...')`
2. `page.get_by_label('...')`
3. `page.get_by_text('...')`
4. stable IDs or semantic attributes (`data-testid`, `aria-label`)
5. CSS classes only as a last resort

## Evidence Rules

- Always set viewport to 1280x1800.
- Do not use `full_page=True`; verify the visible state that a user would see.
- Print URL and title after navigation.
- Print ARIA snapshots for the region being controlled.
- Save screenshots for each critical point in final runs.
- Inspect screenshots with `vision_analyze` when visual state is load-bearing.
