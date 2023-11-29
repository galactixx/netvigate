from typing import Dict, List

from netvigate.prompts.utils import PromptHarvesterJSON

class Memory:
    """Brief class to keep track of memory of llm based on tasks."""
    def __init__(self, user_request: str):
        self._user_request = user_request

        self._completed_tasks: List[Dict[str, str]] = []

    def completed_memory_add(self, task_detail: Dict[str, str]) -> None:
        """Add to completed task memory once task is verified as complete."""

        self._completed_tasks.append(task_detail)

    def completed_memory_templatize(self) -> str:
        """Templatize completed task memory."""

        return '\n'.join([
            f"{idx+1}) Task: {task[PromptHarvesterJSON.TASK.value]}, Action Taken: {task[PromptHarvesterJSON.ACTION.value]}"
            for idx, task in enumerate(self._completed_tasks)
        ])