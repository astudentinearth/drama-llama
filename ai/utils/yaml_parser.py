# utils/yaml_parser.py

from typing import Any, Dict
import yaml

class YamlParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = dict()
    def parse(self):
        with open(self.file_path, 'r') as file:
            self.data = yaml.safe_load(file)
        return self.data

    def get_keys(self) -> list[str]:
        return list(self.data.keys())

    def get_value(self, key: str) -> Any:
        return self.data[key]

    def get_values(self) -> list[Any]:
        return list(self.data.values())

    