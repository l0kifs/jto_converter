from dataclasses import is_dataclass, fields, Field
from typing import get_origin, get_args, TypeVar


class JsonParser:
    T = TypeVar('T')

    @classmethod
    def parse_json(cls, dataclass_type: T, json_data: dict) -> T:
        if not is_dataclass(dataclass_type):
            raise ValueError(f'Dataclass type expected, but received "{str(type(dataclass_type))}"')
        result = cls.__parse_dict(dataclass_type, json_data)
        return result

    @classmethod
    def __parse_dict(cls, dataclass_type: T, json_data: dict):
        dataclass_obj: dataclass_type = dataclass_type()
        for dataclass_field in fields(dataclass_type):
            cls.__parse_dict_item(dataclass_field, json_data, dataclass_obj)
        return dataclass_obj

    @classmethod
    def __parse_dict_item(cls, class_field: Field, json_data: dict, result_class):
        for key, value in json_data.items():
            if class_field.metadata['name'] == key:
                type_args = get_args(class_field.type)
                is_nullable = True
                if type(None) in type_args:
                    field_type = class_field.type.__args__[0]
                else:
                    is_nullable = False
                    field_type = class_field.type

                if value is None:
                    if not is_nullable:
                        raise ValueError(f'Field "{class_field.metadata["name"]}" cannot be null')
                    else:
                        setattr(result_class, key, None)
                else:
                    if is_dataclass(field_type):
                        setattr(result_class, key, cls.__parse_dict(field_type, value))
                    elif str(field_type)[:11] == 'typing.List':
                        setattr(result_class, key, cls.__parse_list(field_type, value))
                    else:
                        if field_type != type(value):
                            raise TypeError(f'Expected value type is "{str(field_type)}", '
                                            f'but received "{str(type(value))}"')
                        setattr(result_class, key, value)
                return

        if class_field.metadata['required']:
            raise ValueError(f'Required field "{class_field.name}" not found in the data "{json_data}"')

    @classmethod
    def __parse_list(cls, class_field_type, json_value: list):
        if get_origin(class_field_type) != list or get_args(class_field_type) == ():
            raise ValueError(f'class_field type "{str(class_field_type)}" is not a supported list. '
                             f'Change type to List[YourClass]')
        if type(json_value) != list:
            raise ValueError(f'json_value type "{str(type(json_value))}" is not a list.')

        class_type = get_args(class_field_type)[0]

        items = []
        if is_dataclass(class_type):
            for item in json_value:
                final_item = cls.__parse_dict(class_type, item)
                items.append(final_item)
        else:
            items.extend(json_value)

        return items
