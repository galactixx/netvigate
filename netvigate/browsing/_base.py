from typing import Tuple

from abc import ABC, abstractmethod

SizeType = Tuple[int, int]

class BaseBrowser(ABC):
    @abstractmethod
    async def load_webbrowser(self) -> None:
        """Load browser and driver."""
        pass

    @abstractmethod
    async def go_to_page(self, url: str) -> None:
        """Open up url in webpage."""
        pass

    @abstractmethod
    async def exit_browser(self) -> None:
        """Exit webpage."""
        pass

    @abstractmethod
    async def exit_driver(self) -> None:
        """Exit playwright driver."""
        pass

    @abstractmethod
    async def page_to_dom(self) -> str:
        """Extracts the DOM from a webpage."""
        pass

    @abstractmethod
    async def page_to_screenshot(self) -> bytes:
        """Takes screenshot of current webpage."""
        pass

    @abstractmethod
    async def page_window_size(self) -> SizeType:
        """Get size of browser window."""
        pass

    @abstractmethod
    async def page_viewport_size(self) -> SizeType:
        """Set size of viewport."""
        pass

    @abstractmethod
    async def page_webpage_size(self) -> SizeType:
        """Set size of entire webpage."""
        pass