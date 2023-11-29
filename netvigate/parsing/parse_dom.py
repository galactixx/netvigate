from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
from bs4 import Tag

# DOM parsing types
ElementType = List[Tuple[str, Tag]]
PageSourceIndexType = Dict[int, Dict[str, Tag]]

INTERACTABLE_TAGS = {
    'a': 'link',
    'button': 'button',
    'input': 'input',
    'textarea': 'input text',
    'select': 'drop-down list'}

def generate_css_selector(tag: str, element: Tag) -> str:
    """Geneate a relevant CSS selector when an element is identified."""

    if tag == 'a':
        attribute_href = element.get('href')
        return f'a[href="{attribute_href}"]'

    for attribute in ['id', 'class', 'aria-label']:
        attribute_result = element.get(attribute)
        if attribute_result is not None:
            return f'{attribute}="{attribute_result}"'
        
    element_string = str(element).split()[1].strip()
    element_string_attibute = element_string.split('=')[0].strip()
    element_string_attribute_result = element_string.split('=')[1].strip()
    return f'{element_string_attibute}="{element_string_attribute_result}"'

def retrieve_page_source_elements(page_source: str) -> ElementType:
    """Parse the page source and retrieve all interactable elements."""

    interactable_elements = []
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all anchor link, button, input and select tags
    for tag in INTERACTABLE_TAGS:
        if tag == 'a':
            elements = soup.find_all(tag, href=True)
        else:
            elements = soup.find_all(tag)
        for element in elements:
            interactable_elements.append((tag, element))

    return interactable_elements

def index_page_source_elements(elements: ElementType) -> PageSourceIndexType:
    """Take list of page source elements and index and make more concise."""

    page_source_index = {}
    for idx, (tag, element) in enumerate(elements):
        page_source_index.update({idx+1: {'Tag': tag, 'Element': element}})

    return page_source_index

def templatize_page_source_index(page_source_index: PageSourceIndexType) -> str:
    """Templatize the page source index into an acceptable prompt."""

    template = ''
    for id, data in page_source_index.items():

        # Retrieve data from dictionary
        tag = data['Tag']
        element = data['Element']

        # Retrieve relevant attributes from element
        description = ''
        aria_label = element.get('aria-label')

        if aria_label is not None:
            text = element.text
            description += aria_label
        elif text != '':
            description += text
        else:
            for attribute in ['class', 'id']:
                attribute_result = element.get(attribute)
                if attribute_result is not None:
                    if isinstance(attribute_result, list):
                        attribute_result = attribute_result[0]
                    description = attribute_result
                    break

        # Compile relevant info into "description" for LLM
        tag_new = INTERACTABLE_TAGS[tag]
        element_body = f'element={tag_new} info={description.strip()}'
        if element_body in template:
            continue
        
        element_info = f'id={id} {element_body}\n'
            
        if description == '':
            continue
        
        template += element_info

    return template