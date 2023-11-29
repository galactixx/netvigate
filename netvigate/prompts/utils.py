from enum import Enum

class PromptInitialJSON(Enum):
    URL = 'url'

class PromptHarvesterJSON(Enum):
    ELEMENT_ID = 'element_id'
    ACTION = 'action'
    TEXT = 'text'
    TASK = 'task'
    URL = 'url'
    COMPLETED = 'completed'

FIELDS_INITIAL_PROMPT = [i.value for i in PromptInitialJSON]
FIELDS_HARVESTER_PROMPT = [i.value for i in PromptHarvesterJSON]