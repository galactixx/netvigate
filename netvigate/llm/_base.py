from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def initialize_request_chain(self) -> None:
        pass

    @abstractmethod
    def get_completion(self, content: str) -> str:
        pass