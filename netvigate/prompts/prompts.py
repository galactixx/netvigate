PROMPT_INITIAL = """
You are browsing the web needing to complete a task.
Your decisions must always be made independently without seeking user assistance.

User Request: {user_request}

We need to navigate to an initial website. Please include url of website.

Your response needs to be in the exact json format shown below:

{{
    "url": <url>
}}
"""

PROMPT_HARVESTER = """
You are browsing the web needing to complete a task.
Your decisions must always be made independently without seeking user assistance.

User Request: {user_request}

Completed Tasks:
{completed_tasks}

You need to make two main decisions.
1) What HTML element is relevant to complete the immediate task.
2) What action to take with that HTML element.

The actions are:
1) click
    - Function to click on a url or button
2) type
    - Function to type text in an input/text area and hit the enter key
3) go_to_url
    - Navigates to a specific URL

Whenever the action type is selected, the enter key is always selected.

Below are the HTML elements. Please choose one that matches with your current task.
{html_elements}

Your response needs to be in the exact json format shown below:

The text field should be None if the action is not type.
The task field should be a brief one sentence description of the current task.
The completed field should be True if the current task will complete the user request.
The url field should be None if the action is not go_to_url.

{{
    "element_id": int,
    "action": str,
    "text": str or "None",
    "task": str
    "url": str or "None",
    "completed": "True" or "False"
}}
"""