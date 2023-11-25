from typing import Tuple

from abc import ABC, abstractmethod

SizeType = Tuple[int, int]

class BaseBrowser(ABC):
    @abstractmethod
    def page_to_dom(self) -> str:
        """Extracts the DOM from a webpage."""
        pass

    @abstractmethod
    def page_to_screenshot(self) -> bytes:
        """Takes screenshot of current webpage."""
        pass

    @abstractmethod
    def page_window_size(self) -> SizeType:
        """Get size of browser window."""
        pass

    @abstractmethod
    def page_viewport_size(self) -> SizeType:
        """Set size of viewport."""
        pass

    @abstractmethod
    def page_webpage_size(self) -> SizeType:
        """Set size of entire webpage."""
        pass