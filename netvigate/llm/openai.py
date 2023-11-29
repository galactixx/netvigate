import os

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
        
        self._messages = []

    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from OpenAI API."""

        self._messages.append({"role": "user", "content": prompt})

        # Chat completion
        response = self._client.chat.completions.create(
            model=self._model_name.value,
            messages=self._messages,
            temperature=self._temperature,
            stream=False,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content