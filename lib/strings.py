import re
from typing import Any, Callable, TypeVar, cast

def camel_to_snake(name: str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(name: str):
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

T = TypeVar('T')
def process_keys_recursive(obj: T, converter: Callable[[str], str]) -> T:
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = converter(k)
            new_dict[new_key] = process_keys_recursive(v, converter)
        return cast(T, new_dict)
    elif isinstance(obj, list):
        return cast(T, [process_keys_recursive(i, converter) for i in obj])
    else:
        return obj
