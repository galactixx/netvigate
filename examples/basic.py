from netvigate.browsing.selenium import SeleniumBrowser

browser = SeleniumBrowser()

browser.go_to_page(url='https://www.google.com')

dom = browser.page_to_dom()
print(dom)