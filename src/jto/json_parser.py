import logging
from dataclasses import is_dataclass, fields, Field
from types import NoneType
from typing import get_origin, get_args, TypeVar, Any


class JsonParser:
    _log = logging.getLogger(__name__)
    T = TypeVar('T')

    @classmethod
    def parse_json(cls, dataclass_type: T,
                   json_data: dict) -> T:
        cls._log.debug('Parsing json to dataclass object')

        if not is_dataclass(dataclass_type):
            cls._log.error(f'Dataclass type expected, but received "{str(type(dataclass_type))}"', exc_info=True)
            raise ValueError(f'Dataclass type expected, but received "{str(type(dataclass_type))}"')
        result = cls._parse_dict(dataclass_type, json_data)
        return result

    @classmethod
    def _parse_dict(cls, dataclass_type: T,
                    json_data: dict) -> T:
        cls._log.debug('Parsing dict to dataclass object')

        dataclass_obj: dataclass_type = dataclass_type()
        for dataclass_field in fields(dataclass_type):
            cls._parse_dict_item(dataclass_field, json_data, dataclass_obj)
        return dataclass_obj

    @classmethod
    def _is_field_nullable(cls, field: Field) -> bool:
        cls._log.debug(f'Checking if field "{field.name}" is nullable')

        type_args = get_args(field.type)
        if NoneType in type_args:
            return True
        else:
            return False

    @classmethod
    def _get_field_type(cls, field: Field) -> type:
        cls._log.debug(f'Getting type of field "{field.name}"')

        type_args = get_args(field.type)
        if NoneType in type_args:
            return [arg for arg in type_args if arg is not NoneType][0]
        else:
            return field.type

    @classmethod
    def _validate_field_value(cls, class_field: Field,
                              value: Any) -> None:
        cls._log.debug(f'Validating value "{value}" of field "{class_field.name}"')
        metadata_key = 'validate'

        if metadata_key not in class_field.metadata:
            return
        if not callable(class_field.metadata[metadata_key]):
            cls._log.error(f'Value of metadata key "{metadata_key}" is not callable', exc_info=True)
            raise ValueError(f'Value of metadata key "{metadata_key}" is not callable')

        validate_func = class_field.metadata[metadata_key]

        if not validate_func(value):
            cls._log.error(f'Value "{value}" of field "{class_field.name}" is not valid', exc_info=True)
            raise ValueError(f'Value "{value}" of field "{class_field.name}" is not valid')

    @classmethod
    def _parse_dict_item(cls, class_field: Field,
                         json_data: dict,
                         result_obj):
        cls._log.debug(f'Parsing dict item "{class_field.name}"')

        for key, value in json_data.items():
            if class_field.metadata['name'] == key:
                is_nullable = cls._is_field_nullable(class_field)
                field_type = cls._get_field_type(class_field)

                if value is None:
                    if not is_nullable:
                        cls._log.error(f'Field "{class_field.metadata["name"]}" cannot be null', exc_info=True)
                        raise ValueError(f'Field "{class_field.metadata["name"]}" cannot be null')
                    else:
                        setattr(result_obj, class_field.name, value)
                        return

                if is_dataclass(field_type):
                    setattr(result_obj, class_field.name, cls._parse_dict(field_type, value))
                    return
                elif get_origin(field_type) == list:
                    setattr(result_obj, class_field.name, cls._parse_list(class_field, field_type, value))
                    return
                else:
                    if field_type != type(value):
                        cls._log.error(f'Expected value type is "{str(field_type)}", '
                                       f'but received "{str(type(value))}"', exc_info=True)
                        raise TypeError(f'Expected value type is "{str(field_type)}", '
                                        f'but received "{str(type(value))}"')
                    cls._validate_field_value(class_field, value)
                    setattr(result_obj, class_field.name, value)
                    return

        if class_field.metadata['required']:
            cls._log.error(f'Required field "{class_field.name}" not found in the data "{json_data}"', exc_info=True)
            raise ValueError(f'Required field "{class_field.name}" not found in the data "{json_data}"')

    # method currently not used because of upper level validations
    # @classmethod
    # def _validate_list(cls, field_type, value):
    #     cls._log.debug('Validating list field and its value')
    #
    #     if get_origin(field_type) != list:
    #         cls._log.error(f'class_field type "{str(field_type)}" is not a list', exc_info=True)
    #         raise TypeError(f'class_field type "{str(field_type)}" is not a list')
    #
    #     if get_args(field_type) == ():
    #         cls._log.error(f'class_field type "{str(field_type)}" is not a supported list. '
    #                        f'Change type to List[YourClass]', exc_info=True)
    #         raise TypeError(f'class_field type "{str(field_type)}" is not a supported list. '
    #                         f'Change type to List[YourClass]')
    #
    #     if not isinstance(value, list):
    #         cls._log.error(f'json_value type "{str(type(value))}" is not a list.', exc_info=True)
    #         raise TypeError(f'json_value type "{str(type(value))}" is not a list.')

    @classmethod
    def _parse_list(cls, class_field: Field,
                    class_field_type,
                    json_value: list) -> list:
        cls._log.debug('Parsing list')
        # cls._validate_list(class_field_type, json_value)

        list_item_type = get_args(class_field_type)[0]

        items = []
        if is_dataclass(list_item_type):
            for item in json_value:
                final_item = cls._parse_dict(list_item_type, item)
                items.append(final_item)
        else:
            cls._validate_field_value(class_field, json_value)
            items.extend(json_value)

        return items
