from playwright.sync_api import sync_playwright

class PlaywrightBrowser:
    """Direct methods for browsing."""
    def __init__(self, headless: bool = False):
        self._headless = headless

        # Instantiate a Chrome browser
        self._driver = sync_playwright().start()
        self._browser = self._driver.chromium.launch(headless=self._headless)

    def go_to_page(self, url: str) -> None:
        """Open up url in webpage."""
        page = self._browser.new_page()
        page.goto(url)

    def exit_browser(self) -> None:
        """Exit webpage."""
        self._browser.close()

    def exit_driver(self) -> None:
        """Exit playwright driver."""
        self._driver.stop()