from playwright.sync_api import Page, sync_playwright
from netvigate.browsing._base import BaseBrowser, SizeType

class PlaywrightBrowser(BaseBrowser):
    """Playwright browsing interface with helper methods."""
    def __init__(self, headless: bool = False):
        self._headless = headless

        # Instantiate a Chrome browser
        self._driver = sync_playwright().start()
        self._browser = self._driver.chromium.launch(headless=self._headless)
        self._page: Page = None

    def go_to_page(self, url: str) -> None:
        self._page = self._browser.new_page()
        self._page.goto(url)

    def exit_browser(self) -> None:
        self._browser.close()

    def exit_driver(self) -> None:
        self._driver.stop()

    def page_to_dom(self) -> str:
        self._page.wait_for_load_state("load")
        return self._page.content()

    def page_to_screenshot(self) -> bytes:
        return self._page.screenshot(full_page=True)
    
    def page_window_size(self) -> None:
        raise NotImplementedError("This function is not implemented.")

    def page_viewport_size(self) -> SizeType:
        viewport_size = self._page.viewport_size()
        width = viewport_size['width']
        height = viewport_size['height']
        return width, height

    def page_webpage_size(self) -> SizeType:
        width = self._page.evaluate("document.documentElement.scrollWidth")
        height = self._page.evaluate("document.documentElement.scrollHeight")
        return width, height