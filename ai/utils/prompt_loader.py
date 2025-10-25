# utils/prompt_loader.py

import os
import yaml
from typing import Dict, Any
from utils import YamlParser

class PromptLoader:
    """
    PromptLoader that loads prompts fresh every time (no caching).
    This ensures prompt changes are always picked up immediately.
    """
    
    def __init__(self) -> None:
        """Initialize with prompts directory path."""
        self.directory: str = os.path.join(os.path.dirname(__file__), '../prompts')
    
    def get_prompt(self, name: str) -> Dict[str, Any]:
        """
        Get a prompt by name. Loads fresh from disk every time.
        
        Args:
            name: Name of the prompt (without .prompt.yaml extension)
            
        Returns:
            Dict with prompt data
            
        Raises:
            ValueError: If prompt file not found
        """
        # lowercase the name for case-insensitive matching
        name = name.lower()
        
        # Build full file path
        prompt_file = f"{name}.prompt.yaml"
        file_path = os.path.join(self.directory, prompt_file)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise ValueError(f"Prompt '{name}' not found at {file_path}")
        
        # Load and parse the YAML file
        with open(file_path, 'r', encoding='utf-8') as file:
            prompt_data = YamlParser(file_path=file.name).parse()
        
        return prompt_data
    
    @classmethod
    def reset(cls) -> None:
        """Reset method for compatibility (no-op since we don't cache)."""
        pass