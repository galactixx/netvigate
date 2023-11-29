import json
from typing import Optional, Union
import time

from netvigate.memory.memory import Memory
from netvigate.llm.openai import OpenAILLM
from netvigate.prompts.prompts import PROMPT_HARVESTER, PROMPT_INITIAL
from netvigate.browsing.playwright import PlaywrightBrowser
from netvigate.browsing.selenium import SeleniumBrowser
from netvigate.prompts.utils import (
    FIELDS_HARVESTER_PROMPT,
    FIELDS_INITIAL_PROMPT,
    PromptHarvesterJSON,
    PromptInitialJSON)
from netvigate.parsing.parse_dom import (
    generate_css_selector,
    index_page_source_elements,
    retrieve_page_source_elements,
    templatize_page_source_index
)

BrowserType = Union[SeleniumBrowser, PlaywrightBrowser]

class Harvester:
    """
    AI browsing agent that does not write code but just selects or 'harvests' the relevant HTML elements.
    """
    def __init__(self, browser: BrowserType, llm: OpenAILLM):
        self._browser = browser
        self._llm = llm

        self._MAX_RETRIES = 5

    def _json_validation(self, response: str, keys_expected: list) -> Optional[str]:
        """Validate json output from LLM as what is expected."""

        try:
            data: dict = json.loads(response)
        except json.JSONDecodeError:
            return
        
        # Checking if all expected keys are present
        missing_keys = [key for key in keys_expected if key not in data]
        if missing_keys:
            return
        
        # Fix formatting; turn "None" to None and "False"/"True" to False/True
        if len(data) > 1:
            for key in [PromptHarvesterJSON.TEXT, PromptHarvesterJSON.URL]:
                if data[key.value] == "None":
                    data.update({key.value: None})
            data.update(
                {PromptHarvesterJSON.COMPLETED.value: data[PromptHarvesterJSON.COMPLETED.value].lower() == "true"})
        
        return data
    
    def _take_action(self, css_selector: str, element: dict, response: dict) -> None:
        """Take action logic once element has been decided upon."""

        tag = element['Tag']
        action = response[PromptHarvesterJSON.ACTION.value]
        if action == 'type':
            self._browser.type_input(
                tag=tag,
                text=response[PromptHarvesterJSON.TEXT.value],
                selector=css_selector)
        elif action == 'click':
            self._browser.click_on_selection(selector=css_selector)

    def _parse_response_json(self, content: str, previous_task: str, keys_expected: list) -> Optional[dict]:
        """Parse response JSON from LLM."""

        counter = 0
        while True:
            response = self._llm.get_completion(content=content, previous_task=previous_task)
            response_json = self._json_validation(response=response, keys_expected=keys_expected)

            if response_json is None:
                counter += 1
            
            if counter > self._MAX_RETRIES:
                return
            
            return response_json

    def harvest(self, user_request: str) -> None:
        """Implement AI browsing given a prompt from user."""

        if not user_request:
            raise ValueError('task is empty or None, task must be a non-empty string')

        # Initialize memory
        memory = Memory(user_request=user_request)
        self._llm.initialize_request_chain(user_request=user_request)

        # Navigation to an initial url
        response_json = self._parse_response_json(
            content=PROMPT_INITIAL.format(user_request=user_request),
            previous_task=None,
            keys_expected=FIELDS_INITIAL_PROMPT)
        url = response_json[PromptInitialJSON.URL.value]

        self._browser.go_to_page(url=url)
        previous_task = f'navigate to {url}'

        while True:

            # Retrieve DOM from page
            page_source = self._browser.page_to_dom()

            # Parse DOM of webpage
            page_source_elements = retrieve_page_source_elements(page_source=page_source)
            page_source_index = index_page_source_elements(elements=page_source_elements)

            # Templatize page source elements
            page_source_templatized = templatize_page_source_index(page_source_index=page_source_index)

            # Get LLM completion and validate
            completed_tasks = memory.completed_memory_templatize()
            response_json = self._parse_response_json(
                content=PROMPT_HARVESTER.format(
                    user_request=user_request,
                    completed_tasks=completed_tasks,
                    html_elements=page_source_templatized),
                previous_task=previous_task,
                keys_expected=FIELDS_HARVESTER_PROMPT
            )
            previous_task = response_json.get(PromptHarvesterJSON.TASK.value)

            # Retrieve relevant element from page_source_index
            element = page_source_index[response_json[PromptHarvesterJSON.ELEMENT_ID.value]]

            css_selector = generate_css_selector(tag=element['Tag'], element=element['Element'])
            self._take_action(css_selector=css_selector, element=element, response=response_json)

            # Add to memory of completed tasks
            memory.completed_memory_add(task_detail=response_json)

            if response_json[PromptHarvesterJSON.COMPLETED.value]:
                time.sleep(4)
                break

        # # Close browser
        self._browser.exit_browser()