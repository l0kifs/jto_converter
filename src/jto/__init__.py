import logging
from typing import TypeVar

from jto.json_builder import JsonBuilder
from jto.json_parser import JsonParser


class JTOConverter:
    _log = logging.getLogger(__name__)
    T = TypeVar('T')

    @classmethod
    def from_json(cls, dataclass_type: T,
                  json_data: dict) -> T:
        """
        Convert json to dataclass object
        :param dataclass_type: dataclass type object
        :param json_data: json data
        :return: dataclass object
        """
        cls._log.debug('Converting json to dataclass object')
        result = JsonParser.parse_json(dataclass_type, json_data)
        return result

    @classmethod
    def to_json(cls, dataclass_obj) -> dict:
        """
        Convert dataclass object to json
        :param dataclass_obj: dataclass object
        :return: json object
        """
        cls._log.debug('Converting dataclass object to json')
        result = JsonBuilder.build_json(dataclass_obj)
        return result
