from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumBrowser:
    """Direct methods for browsing."""
    def __init__(self, headless: bool = False):
        self._headless = headless

        # Instantiate a Chrome browser
        self._driver = webdriver.Chrome(ChromeDriverManager().install())

    def go_to_page(self, url: str) -> None:
        """Open up url in webpage."""
        self._driver.get(url)

    def exit_browser(self) -> None:
        """Exit webpage."""
        self._driver.quit()