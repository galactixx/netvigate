import os

from selenium import webdriver
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

class SeleniumBrowser:
    """Direct methods for browsing."""
    def __init__(self, headless: bool = False):
        self._headless = headless

        # Check Chrome executable path
        _is_chromedriver_in_path()

        # Instantiate a Chrome browser
        self._options = Options()
        self.driver = webdriver.Chrome(options=self._options)

    def go_to_page(self, url: str) -> None:
        """Open up url in webpage."""
        self.driver.get(url)

    def exit_browser(self) -> None:
        """Exit webpage."""
        self.driver.quit()