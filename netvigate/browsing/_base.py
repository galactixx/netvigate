from typing import Tuple
import time

from abc import ABC, abstractmethod

SizeType = Tuple[int, int]

class BaseBrowser(ABC):
    @abstractmethod
    def _wait_for_load(self) -> None:
        """Wait for webpage to load before proceeding with actions."""
        pass

    @abstractmethod
    def click_on_selection(self) -> None:
        """Click on selection (button, etc.)."""
        pass

    @abstractmethod
    def type_input(self) -> None:
        """Type text into input."""
        pass

    @abstractmethod
    def go_to_page(self, url: str) -> None:
        """Open up url in webpage."""
        pass

    @abstractmethod
    def exit_browser(self) -> None:
        """Exit webpage."""
        pass

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