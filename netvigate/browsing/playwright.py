from playwright.async_api import (
    async_playwright,
    Browser,
    Page, 
    Playwright)

from netvigate.browsing._base import BaseBrowser, SizeType

class PlaywrightBrowser(BaseBrowser):
    """Playwright browsing interface with helper methods."""
    def __init__(self, headless: bool = False):
        self._headless = headless

        self._driver: Playwright = None
        self._browser: Browser = None

        self._page: Page = None

    async def load_webbrowser(self) -> None:
        self._driver = await async_playwright().start()
        self._browser = await self._driver.chromium.launch(headless=self._headless)

    async def go_to_page(self, url: str) -> None:
        self._page = await self._browser.new_page()
        await self._page.goto(url)

    async def exit_browser(self) -> None:
        await self._browser.close()

    async def exit_driver(self) -> None:
        await self._driver.stop()

    async def page_to_dom(self) -> str:
        content = await self._page.content()
        return content

    async def page_to_screenshot(self) -> bytes:
        screenshot = await self._page.screenshot(full_page=True)
        return screenshot
    
    async def page_window_size(self) -> None:
        raise NotImplementedError("This function is not implemented.")

    async def page_viewport_size(self) -> SizeType:
        viewport_size = await self._page.viewport_size()
        width = viewport_size['width']
        height = viewport_size['height']
        return width, height

    async def page_webpage_size(self) -> SizeType:
        width = await self._page.evaluate("document.documentElement.scrollWidth")
        height = await self._page.evaluate("document.documentElement.scrollHeight")
        return width, height