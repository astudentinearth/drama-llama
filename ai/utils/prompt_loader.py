# utils/prompt_loader.py

import os
import yaml
from ai.utils import YamlParser

class PromptLoader:
    def __init__(self):
        self.directory = os.path.join(os.path.dirname(__file__), '../prompts')
        self.prompts = {}

    def load_prompts(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.yaml'):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    self.prompts[filename] = YamlParser(file_path=file.name).parse()
        return self.prompts
    
    def get_prompt(self, name):
        # lowercase the name for case-insensitive matching
        name = name.lower()
        
        # if the name match with name.prompt.yaml, return that prompt
        prompt_file = f"{name}.prompt.yaml"
        if prompt_file in self.prompts:
            return self.prompts[prompt_file]
        raise ValueError(f"Prompt '{name}' not found.")