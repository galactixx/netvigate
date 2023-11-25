from netvigate.browsing.selenium import SeleniumBrowser
from netvigate.browsing_utils._base import BaseBrowser, SizeType

class SeleniumBrowserUtils(BaseBrowser):
    """Selenium browsing interface with helper methods."""
    def __init__(self, browser: SeleniumBrowser):
        self._browser = browser

    def page_to_dom(self) -> str:
        return self._browser.driver.page_source

    def page_to_screenshot(self) -> bytes:
        return self._browser.driver.get_screenshot_as_png()
    
    def page_window_size(self) -> SizeType:
        size = self._browser.driver.get_window_size()
        return size['width'], size['height']

    def page_viewport_size(self) -> SizeType:
        width = self._browser.driver.execute_script("return window.innerWidth;")
        height = self._browser.driver.execute_script("return window.innerHeight;")
        return width, height

    def page_webpage_size(self) -> SizeType:
        width = self._browser.driver.execute_script("return document.documentElement.scrollWidth;")
        height = self._browser.driver.execute_script("return document.documentElement.scrollHeight;")
        return width, height