from dataclasses import is_dataclass, asdict

from jto.undefined_field import Undefined


class JsonBuilder:
    @classmethod
    def to_json(cls, dataclass_obj, drop_nones: bool) -> dict:
        if not is_dataclass(dataclass_obj):
            raise ValueError(f'Dataclass type object expected, but received "{str(type(dataclass_obj))}"')

        result = asdict(dataclass_obj)
        result = cls.__drop_undefined(result)
        if drop_nones:
            result = cls.__drop_nones(result)
        return result

    @classmethod
    def __drop_undefined(cls, original_dict: dict) -> dict:
        result_dict = {}
        for key, value in original_dict.items():
            if value != Undefined:
                if isinstance(value, dict):
                    result_dict[key] = cls.__drop_undefined(value)
                elif isinstance(value, (list, set, tuple)):
                    result_dict[key] = cls.__drop_undefined_in_list(value)
                else:
                    result_dict[key] = value
        return result_dict

    @classmethod
    def __drop_undefined_in_list(cls, original_list: list) -> list:
        result_list = []
        for value in original_list:
            if value != Undefined:
                if isinstance(value, dict):
                    result_list.append(cls.__drop_undefined(value))
                elif isinstance(value, (list, set, tuple)):
                    result_list.append(cls.__drop_undefined_in_list(value))
                else:
                    result_list.append(value)
        return result_list

    @classmethod
    def __drop_nones(cls, original_dict: dict) -> dict:
        result_dict = {}
        for key, value in original_dict.items():
            if isinstance(value, dict):
                result_dict[key] = cls.__drop_nones(value)
            elif isinstance(value, (list, set, tuple)):
                result_dict[key] = cls.__drop_nones_in_list(value)
            elif value is not None:
                result_dict[key] = value
        return result_dict

    @classmethod
    def __drop_nones_in_list(cls, original_list: list) -> list:
        result_list = []
        for value in original_list:
            if isinstance(value, dict):
                result_list.append(cls.__drop_nones(value))
            elif isinstance(value, (list, set, tuple)):
                result_list.append(cls.__drop_nones_in_list(value))
            else:
                result_list.append(value)
        return result_list
