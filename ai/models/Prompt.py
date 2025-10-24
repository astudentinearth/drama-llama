from ai.utils import PromptLoader

class Prompt:
    def __init__(self, name: str, format):
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
        if 'messages' in prompt_data:
            for message in prompt_data['messages']:
                if 'content' in message:
                    for key, value in self.format.items():
                        # Convert value to string to handle lists and other types
                        str_value = str(value) if not isinstance(value, str) else value
                        # Match both {{key}} and {{ key }} patterns
                        message['content'] = message['content'].replace(f"{{{{{key}}}}}", str_value)
                        message['content'] = message['content'].replace(f"{{{{ {key} }}}}", str_value)
        return prompt_data
    
    def get_prompt(self):
        """Returns the full prompt data structure"""
        return self.prompt_data
    
    def get_messages(self):
        """Returns just the messages array"""
        return self.prompt_data.get('messages', [])