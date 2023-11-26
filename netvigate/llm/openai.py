from openai import OpenAI

from netvigate.llm._base import BaseLLM
from netvigate.llm._models import OpenAIModels

class OpenAILLM(BaseLLM):
    """Simple interface for OpenAI LLM."""
    def __init__(self,
                 api_key: str,
                 model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO_INSTRUCT,
                 temperature: float = 0.70):
        self._api_key = api_key
        self._model_name = model_name
        self._temperature = temperature

        # Instantiate a client object for interacting with the OpenAI API
        self._client = OpenAI(api_key=self._api_key)

        if not isinstance(self._model_name, OpenAIModels):
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from OpenAI API."""

        # Chat completion
        response = self._client.completions.create(
            model=self._model_name.value,
            prompt=prompt,
            temperature=self._temperature,
            stream=False,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].text