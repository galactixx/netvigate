from netvigate.browsing.playwright import PlaywrightBrowser

def run(url: str) -> None:

    # Set-up initial playwright browser
    browser = PlaywrightBrowser()

    # Go to page
    browser.go_to_page(url=url)

    # Retrieve DOM
    dom = browser.page_to_dom()
    print(f'Length of DOM: {len(dom)}')

    # Close browser
    browser.exit_browser()

if __name__ == "__main__":
    run(url='https://www.google.com')