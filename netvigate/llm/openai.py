import os
from typing import Dict, List, Optional

from openai import OpenAI

from netvigate.llm._base import BaseLLM
from netvigate.llm._models import OpenAIModels

class OpenAILLM(BaseLLM):
    """Simple interface for OpenAI LLM."""
    def __init__(self,
                 model_name: OpenAIModels = OpenAIModels.GPT_4,
                 temperature: float = 0.70):
        self._model_name = model_name
        self._temperature = temperature

        self._api_key = os.environ.get("OPENAI_API_KEY")

        # The API key is blank or not set
        if not self._api_key:
            raise ValueError("OPENAI_API_KEY is not set or is blank")

        # Instantiate a client object for interacting with the OpenAI API
        self._client = OpenAI(api_key=self._api_key)

        if not isinstance(self._model_name, OpenAIModels):
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
        self._current_conversation_history: List[Dict[str, str]] = []

    def initialize_request_chain(self, user_request: str) -> None:
        """Initialize conversation history with user request."""

        self._current_conversation_history.append(
            {"role": "system", "content": user_request})
        
    def get_completion(self, content: str, previous_task: Optional[str] = None) -> str:
        """Get prompt completion from OpenAI API."""

        # Revised conversation history by simplifying messages and reducing token length.
        if previous_task is not None:
            self._current_conversation_history.pop()
            self._current_conversation_history.append(
                {"role": "assistant", "content": previous_task})

        self._current_conversation_history.append(
            {"role": "user", "content": content}
        )

        # Chat completion
        response = self._client.chat.completions.create(
            model=self._model_name.value,
            messages=self._current_conversation_history,
            temperature=self._temperature,
            stream=False,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content