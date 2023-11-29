from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass