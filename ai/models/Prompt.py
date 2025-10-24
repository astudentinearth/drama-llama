from ai.utils import PromptLoader

class Prompt:
    def __init__(self, name: str, format):
        self.name = name
        self.format = format
        
        prompt = self._fetch_prompt()
        self.prompt = self._fill_variables(prompt)
    

    def _fetch_prompt(self):
        # Use PromptLoader to get the prompt content
        loader = PromptLoader()
        return loader.get_prompt(self.name)
    
    def _fill_variables(self, prompt):
        ## Find all variables with {{}} and replace them with values from self.format
        for key, value in self.format.items():
            prompt = prompt.replace(f"{{{{ {key} }}}}", value)
        return prompt