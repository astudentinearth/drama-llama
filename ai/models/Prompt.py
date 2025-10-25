from utils import PromptLoader
from pydantic import BaseModel
from typing import Union, Type, Dict, Any

class Prompt:
    def __init__(self, name: str, format: Union[BaseModel, Type[BaseModel], Dict[str, Any]]):
        self.name = name
        self.format = format
        
        prompt_data = self._fetch_prompt()
        self.prompt_data = self._fill_variables(prompt_data)
    

    def _fetch_prompt(self):
        # Use PromptLoader to get the prompt content
        loader = PromptLoader()
        return loader.get_prompt(self.name)
    
    def _fill_variables(self, prompt_data):
        ## Find all variables with {{}} in messages and replace them with values from self.format
        # Convert BaseModel to dict if needed
        if isinstance(self.format, type) and issubclass(self.format, BaseModel):
            # If it's a BaseModel class (not instance), create an empty dict or use schema
            # For now, we'll skip variable replacement when a class is passed
            format_dict = {}
        elif isinstance(self.format, BaseModel):
            # If it's a BaseModel instance, convert to dict
            format_dict = self.format.model_dump()
        else:
            # If it's already a dict
            format_dict = self.format
        
        if 'messages' in prompt_data:
            for message in prompt_data['messages']:
                if 'content' in message:
                    for key, value in format_dict.items():
                        # Convert value to string to handle lists and other types
                        str_value = str(value) if not isinstance(value, str) else value
                        # Match both {{key}} and {{ key }} patterns
                        message['content'] = message['content'].replace(f"{{{{{key}}}}}", str_value)
                        message['content'] = message['content'].replace(f"{{{{ {key} }}}}", str_value)
        return prompt_data
    
    def get_prompt(self):
        """Returns the full prompt data structure"""
        return self.prompt_data
    
    def get_model(self):
        """Returns just the model name"""
        return self.prompt_data.get('model', '')
    
    def get_system_prompt(self):
        """Returns just the system prompt content"""
        for message in self.prompt_data.get('messages', []):
            if message.get('role') == 'system':
                return message.get('content', '')
        return ''

    def get_user_prompt(self):
        """Returns just the user prompt content"""
        for message in self.prompt_data.get('messages', []):
            if message.get('role') == 'user':
                return message.get('content', '')
        return ''

    def get_messages(self):
        """Returns just the messages array"""
        return self.prompt_data.get('messages', [])