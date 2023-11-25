from abc import ABC, abstractmethod

class BaseBrowser(ABC):

    @abstractmethod
    def page_to_dom(self) -> str:
        """Extracts the DOM from a webpage."""
        pass

    @abstractmethod
    def page_to_javascript(self) -> str:
        """Return javascript output of webpage."""
        pass

    @abstractmethod
    def page_to_screenshot(self) -> None:
        """Takes screenshot of current webpage."""
        pass