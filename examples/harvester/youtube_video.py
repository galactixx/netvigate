from netvigate.agents.harvester import Harvester
from netvigate.browsing.playwright import PlaywrightBrowser
from netvigate.llm.openai import OpenAILLM

def youtube_video_search() -> None:
    """Have the harvester agent find a youtube video based on a description."""

    harvester = Harvester(
        browser=PlaywrightBrowser(), llm=OpenAILLM()
    )

    harvester.harvest(
        user_request="please find a youtube video of jackLNDN at rifflandia festival in 2023")

if __name__ == "__main__":
    youtube_video_search()