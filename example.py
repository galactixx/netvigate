from netvigate.browsing.playwright import PlaywrightBrowser
from netvigate.browsing.selenium import SeleniumBrowser

# playwright = PlaywrightBrowser()

# playwright.go_to_page(url='https://www.google.com/')


selenium = SeleniumBrowser()
selenium.go_to_page('https://www.google.com/')
