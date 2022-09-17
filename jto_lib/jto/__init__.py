from dataclasses import fields, is_dataclass, Field, asdict


class JTOConverter:
    @classmethod
    def __parse_list(cls, class_field, json_value: list):
        if str(class_field.type)[:11] != 'typing.List' or len(str(class_field.type)) < 12:
            raise ValueError(f'class_field type {str(class_field.type)} is not a supported list. '
                             f'Change type to List[YourClass]')
        if type(json_value) != list:
            raise ValueError(f'json_value type {str(type(json_value))} is not a list.')

        class_type = str(class_field.type)[12:-1]
        if class_type.find('__main__.') != -1:
            class_type = class_type.replace('__main__.', '')
        class_type = eval(class_type)

        items = []
        if is_dataclass(class_type):
            for item in json_value:
                final_item = cls.__parse_dict(class_type, item)
                items.append(final_item)
        else:
            items.extend(json_value)

        return items

    @classmethod
    def __parse_dict_item(cls, class_field: Field, json_data: dict, result_class):
        for key, value in json_data.items():
            if class_field.metadata['name'] == key:
                if is_dataclass(class_field.type):
                    setattr(result_class, key, cls.__parse_dict(class_field.type, value))

                elif str(class_field.type)[:11] == 'typing.List':
                    setattr(result_class, key, cls.__parse_list(class_field, value))

                else:
                    # TODO realise type checking if needed. First check if dataclass handles it or not
                    setattr(result_class, key, value)

                return

        if class_field.metadata['required']:
            raise ValueError(f'Required field {class_field.name} not found in the data {json_data}')

    @classmethod
    def __parse_dict(cls, dataclass_type, json_data: dict):
        result = dataclass_type()
        for dataclass_field in fields(dataclass_type):
            cls.__parse_dict_item(dataclass_field, json_data, result)
        return result

    @classmethod
    def from_json(cls, dataclass_type, json_data: dict):
        if not is_dataclass(dataclass_type):
            raise ValueError(f'Dataclass type expected, but received {str(type(dataclass_type))}')

        return cls.__parse_dict(dataclass_type, json_data)

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
    def to_json(cls, dataclass_obj, drop_empty_keys: bool = True):
        if not is_dataclass(dataclass_obj):
            raise ValueError(f'Dataclass type object expected, but received {str(type(dataclass_obj))}')

        result = asdict(dataclass_obj)
        if drop_empty_keys:
            result = cls.__drop_nones(result)
        return result
