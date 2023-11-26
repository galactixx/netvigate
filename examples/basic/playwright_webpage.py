import asyncio

from netvigate.browsing.playwright import PlaywrightBrowser

async def run(url: str) -> None:

    # Set-up initial playwright browser
    browser = PlaywrightBrowser()
    await browser.load_webbrowser()

    # Go to page
    await browser.go_to_page(url=url)

    # Retrieve DOM
    dom = await browser.page_to_dom()
    print(f'Length of DOM: {len(dom)}')

    # Close browser
    await browser.exit_driver()

if __name__ == "__main__":
    asyncio.run(run(url='https://www.google.com'))