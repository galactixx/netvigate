import time

from playwright.sync_api import sync_playwright

from netvigate.browsing._base import (
    BaseBrowser, 
    SizeType)

class PlaywrightBrowser(BaseBrowser):
    """Playwright browsing interface with helper methods."""
    def __init__(self, headless: bool = False, delay: float = 0.5):
        self._delay = delay
        self._browser = (sync_playwright().start()
                         .chromium.launch(headless=headless))

        self._page = self._browser.new_page()

    def _wait_for_load(self) -> None:
        self._page.wait_for_load_state("networkidle")
        self._page.wait_for_function("document.readyState === 'complete'")
        time.sleep(self._delay)

    def click_on_selection(self, selector: str) -> None:
        self._page.click(selector)
        self._wait_for_load()

    def type_input(self, tag: str, text: str, selector: str) -> None:
        self._page.type(f'{tag}[{selector}]', text)
        self._page.keyboard.press('Enter')
        self._wait_for_load()

    def go_to_page(self, url: str) -> None:
        self._page.goto(url, wait_until='load', timeout=10000)
        self._wait_for_load()

    def exit_browser(self) -> None:
        self._browser.close()

    def page_to_dom(self) -> str:
        content = self._page.content()
        return content

    def page_to_screenshot(self) -> bytes:
        screenshot = self._page.screenshot(full_page=True)
        return screenshot
    
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