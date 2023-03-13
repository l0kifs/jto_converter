from typing import TypeVar

from jto.json_builder import JsonBuilder
from jto.json_parser import JsonParser


class JTOConverter:
    T = TypeVar('T')

    @classmethod
    def from_json(cls, dataclass_type: T, json_data: dict) -> T:
        result = JsonParser.parse_json(dataclass_type, json_data)
        return result

    @classmethod
    def to_json(cls, dataclass_obj, drop_nones: bool = False) -> dict:
        result = JsonBuilder.build_json(dataclass_obj, drop_nones)
        return result
