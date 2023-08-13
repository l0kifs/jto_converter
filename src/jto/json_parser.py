from dataclasses import is_dataclass, fields, Field
from typing import get_origin, get_args, TypeVar


class JsonParser:
    T = TypeVar('T')

    @classmethod
    def parse_json(cls, dataclass_type: T,
                   json_data: dict) -> T:
        if not is_dataclass(dataclass_type):
            raise ValueError(f'Dataclass type expected, but received "{str(type(dataclass_type))}"')
        result = cls._parse_dict(dataclass_type, json_data)
        return result

    @classmethod
    def _parse_dict(cls, dataclass_type: T,
                    json_data: dict) -> T:
        dataclass_obj: dataclass_type = dataclass_type()
        for dataclass_field in fields(dataclass_type):
            cls._parse_dict_item(dataclass_field, json_data, dataclass_obj)
        return dataclass_obj

    @classmethod
    def _is_field_nullable(cls, field: Field) -> bool:
        type_args = get_args(field.type)
        if type(None) in type_args:
            return True
        else:
            return False

    @classmethod
    def _get_field_type(cls, field: Field) -> type:
        type_args = get_args(field.type)
        if type(None) in type_args:
            return [arg for arg in type_args if arg != type(None)][0]
        else:
            return field.type

    @classmethod
    def _parse_dict_item(cls, class_field: Field,
                         json_data: dict,
                         result_obj):
        for key, value in json_data.items():
            if class_field.metadata['name'] == key:
                is_nullable = cls._is_field_nullable(class_field)
                field_type = cls._get_field_type(class_field)

                if value is None:
                    if not is_nullable:
                        raise ValueError(f'Field "{class_field.metadata["name"]}" cannot be null')
                    else:
                        setattr(result_obj, key, value)
                else:
                    if is_dataclass(field_type):
                        setattr(result_obj, key, cls._parse_dict(field_type, value))
                    elif get_origin(field_type) == list:
                        setattr(result_obj, key, cls._parse_list(field_type, value))
                    else:
                        if field_type != type(value):
                            raise TypeError(f'Expected value type is "{str(field_type)}", '
                                            f'but received "{str(type(value))}"')
                        setattr(result_obj, key, value)
                return

        if class_field.metadata['required']:
            raise ValueError(f'Required field "{class_field.name}" not found in the data "{json_data}"')

    @classmethod
    def _parse_list(cls, class_field_type,
                    json_value: list) -> list:
        if get_origin(class_field_type) != list:
            raise ValueError(f'class_field type "{str(class_field_type)}" is not a list')
        if get_args(class_field_type) == ():
            raise ValueError(f'class_field type "{str(class_field_type)}" is not a supported list. Change type to List[YourClass]')
        if type(json_value) != list:
            raise ValueError(f'json_value type "{str(type(json_value))}" is not a list.')

        list_item_type = get_args(class_field_type)[0]

        items = []
        if is_dataclass(list_item_type):
            for item in json_value:
                final_item = cls._parse_dict(list_item_type, item)
                items.append(final_item)
        else:
            items.extend(json_value)

        return items
