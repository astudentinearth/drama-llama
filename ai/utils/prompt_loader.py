# utils/prompt_loader.py

import os
import yaml
from typing import Dict, Any, Optional
from utils import YamlParser

class PromptLoader:
    """
    Singleton PromptLoader that loads prompts once and caches them.
    """
    _instance: Optional['PromptLoader'] = None
    _prompts_loaded: bool = False
    
    def __new__(cls) -> 'PromptLoader':
        if cls._instance is None:
            instance = super(PromptLoader, cls).__new__(cls)
            instance.directory = os.path.join(os.path.dirname(__file__), '../prompts')
            instance.prompts = {}
            cls._instance = instance
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize instance variables if not already initialized."""
        if not hasattr(self, 'directory'):
            self.directory: str = os.path.join(os.path.dirname(__file__), '../prompts')
        if not hasattr(self, 'prompts'):
            self.prompts: Dict[str, Any] = {}

    def load_prompts(self) -> Dict[str, Any]:
        """Load prompts from YAML files. Only loads once, subsequent calls use cache."""
        if PromptLoader._prompts_loaded:
            return self.prompts
            
        for filename in os.listdir(self.directory):
            if filename.endswith('.yaml'):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    self.prompts[filename] = YamlParser(file_path=file.name).parse()
        
        PromptLoader._prompts_loaded = True
        return self.prompts
    
    def get_prompt(self, name: str) -> Dict[str, Any]:
        """Get a prompt by name. Automatically loads prompts if not already loaded."""
        # Ensure prompts are loaded
        if not PromptLoader._prompts_loaded:
            self.load_prompts()
        
        # lowercase the name for case-insensitive matching
        name = name.lower()
        
        # if the name match with name.prompt.yaml, return that prompt
        prompt_file = f"{name}.prompt.yaml"
        if prompt_file in self.prompts:
            return self.prompts[prompt_file]
        raise ValueError(f"Prompt '{name}' not found.")
    
    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance and cache. Useful for testing."""
        cls._instance = None
        cls._prompts_loaded = False