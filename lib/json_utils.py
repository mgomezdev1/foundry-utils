from typing import Any, TypeVar, Type
import json

from lib.strings import camel_to_snake, process_keys_recursive, snake_to_camel

T = TypeVar('T')

class JsonUtils:
    @staticmethod
    def from_camel_file(path: str) -> dict[str, Any]:
        with open(path, "r") as f:
            content = f.read()
            return JsonUtils.from_camel_json(content)
        
    @staticmethod
    def from_camel_json(raw_json: str) -> dict[str, Any]:
        data: dict = json.loads(raw_json)
        return JsonUtils.from_camel_dict(data)
    
    @staticmethod
    def from_camel_dict(camel_case_data: Any) -> dict[str, Any]:
        return process_keys_recursive(camel_case_data, camel_to_snake)

    @staticmethod
    def to_camel_json(data: dict) -> str:
        camel_case_data = process_keys_recursive(data, snake_to_camel)
        return json.dumps(camel_case_data, indent=4)
