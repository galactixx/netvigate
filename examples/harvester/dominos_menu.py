from netvigate.agents.harvester import Harvester
from netvigate.browsing.playwright import PlaywrightBrowser
from netvigate.llm.openai import OpenAILLM

def dominos_pizza_menu() -> None:
    """Have the harvester agent google search dominos pizza and navigate to menu."""

    harvester = Harvester(
        browser=PlaywrightBrowser(), llm=OpenAILLM()
    )

    harvester.harvest(
        user_request="google search for dominos pizza and find the menu")

if __name__ == "__main__":
    dominos_pizza_menu()