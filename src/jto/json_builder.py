import logging
from dataclasses import is_dataclass, Field
from types import NoneType
from typing import get_args, get_origin

from jto.undefined_field import Undefined


class JsonBuilder:
    _log = logging.getLogger(__name__)

    @classmethod
    def _is_nullable(cls, field_: Field) -> bool:
        cls._log.debug('Checking if field is nullable')
        type_args = get_args(field_.type)
        if NoneType in type_args:
            return True
        else:
            return False

    @classmethod
    def _is_list_of_dataclasses(cls, field_: Field) -> bool:
        cls._log.debug('Checking if field is list of dataclasses')
        type_args = get_args(field_.type)
        inner_type = field_.type
        if NoneType in type_args:
            inner_type = [arg for arg in type_args if arg is not NoneType][0]
        if get_origin(inner_type) is list:
            if is_dataclass(get_args(inner_type)[0]):
                return True
        return False

    @classmethod
    def _parse_dataclass(cls, dataclass_obj) -> dict:
        cls._log.debug('Parsing dataclass object')
        result_dict = {}
        for field_ in dataclass_obj.__dataclass_fields__.values():
            field_value = getattr(dataclass_obj, field_.name)

            if field_value == Undefined:
                continue

            if field_value is None:
                if not cls._is_nullable(field_):
                    continue
                result_dict[field_.metadata['name']] = None
            elif is_dataclass(field_value):
                result_dict[field_.metadata['name']] = cls._parse_dataclass(field_value)
            elif cls._is_list_of_dataclasses(field_):
                result_list = []
                for item in field_value:
                    result_list.append(cls._parse_dataclass(item))
                result_dict[field_.metadata['name']] = result_list
            else:
                result_dict[field_.metadata['name']] = field_value
        return result_dict

    @classmethod
    def build_json(cls, dataclass_obj) -> dict:
        cls._log.debug('Building json from dataclass object')

        if not is_dataclass(dataclass_obj):
            cls._log.error(f'Dataclass type object expected, but received "{str(type(dataclass_obj))}"', exc_info=True)
            raise TypeError(f'Dataclass type object expected, but received "{str(type(dataclass_obj))}"')

        result_dict = cls._parse_dataclass(dataclass_obj)
        return result_dict
