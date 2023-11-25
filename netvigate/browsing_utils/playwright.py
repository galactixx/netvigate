from netvigate.browsing.playwright import PlaywrightBrowser
from netvigate.browsing_utils._base import BaseBrowser, SizeType

class PlaywrightBrowserUtils(BaseBrowser):
    """Playwright browsing interface with helper methods."""
    def __init__(self, browser: PlaywrightBrowser):
        self._browser = browser

    def page_to_dom(self) -> str:
        self._browser.page.wait_for_load_state("load")
        return self._browser.page.content()

    def page_to_screenshot(self) -> bytes:
        return self._browser.page.screenshot(full_page=True)
    
    def page_window_size(self) -> None:
        raise NotImplementedError("This function is not yet implemented.")

    def page_viewport_size(self) -> SizeType:
        viewport_size = self._browser.page.viewport_size()
        width = viewport_size['width']
        height = viewport_size['height']
        return width, height

    def page_webpage_size(self) -> SizeType:
        width = self._browser.page.evaluate("document.documentElement.scrollWidth")
        height = self._browser.page.evaluate("document.documentElement.scrollHeight")
        return width, height