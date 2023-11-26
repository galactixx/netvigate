import os

from selenium import webdriver
from netvigate.browsing._base import BaseBrowser, SizeType
from selenium.webdriver.chrome.options import Options

def _is_chromedriver_in_path() -> None:
    """Determine the executable name based on the operating system."""
    executable_name = "chromedriver.exe" if os.name == "nt" else "chromedriver"

    # Get the system PATH environment variable
    system_path = os.environ.get('PATH', '')

    # Iterate through each path in the system PATH
    for path_dir in system_path.split(os.pathsep):
        if os.path.isfile(path_dir) and os.path.basename(path_dir) == executable_name:
            return

    raise Exception('path to chromedriver.exe does not exist in path')

class SeleniumBrowser(BaseBrowser):
    """Selenium browsing interface with helper methods."""
    def __init__(self, headless: bool = False):
        self._headless = headless

        # Check Chrome executable path
        _is_chromedriver_in_path()

        # Instantiate a Chrome browser
        self._options = Options()
        self._browser = webdriver.Chrome(options=self._options)

    def go_to_page(self, url: str) -> None:
        self._browser.get(url)

    def exit_browser(self) -> None:
        self._browser.quit()

    def exit_driver(self) -> None:
        raise NotImplementedError("This function is not implemented.")

    def page_to_dom(self) -> str:
        return self._browser.page_source

    def page_to_screenshot(self) -> bytes:
        return self._browser.get_screenshot_as_png()
    
    def page_window_size(self) -> SizeType:
        size = self._browser.get_window_size()
        return size['width'], size['height']

    def page_viewport_size(self) -> SizeType:
        width = self._browser.execute_script("return window.innerWidth;")
        height = self._browser.execute_script("return window.innerHeight;")
        return width, height

    def page_webpage_size(self) -> SizeType:
        width = self._browser.execute_script("return document.documentElement.scrollWidth;")
        height = self._browser.execute_script("return document.documentElement.scrollHeight;")
        return width, height