from dataclasses import dataclass, field


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return ''.join(i.capitalize() for i in s)


@dataclass
class FieldTemplate:
    field_name: str
    field_type: str
    json_field_name: str
    default_value: any = None
    required: bool = False

    def build_field_string(self) -> str:
        field_string = f"{self.field_name}: {self.field_type} = field(default={str(self.default_value)}, " \
                       f"metadata={{'name': '{self.json_field_name}', 'required': {str(self.required)}}})"
        return field_string


@dataclass
class ClassTemplate:
    class_name: str
    class_fields: list = field(default_factory=list)

    def build_class_string(self):
        class_string = f'@dataclass\nclass {self.class_name}:\n'
        class_field_strings = [cls_field.build_field_string() for cls_field in self.class_fields]
        fields_string = '\n    '.join(class_field_strings)
        return class_string+'    '+fields_string


@dataclass
class ClassesTemplate:
    classes: list = field(default_factory=list)

    def build_classes_string(self):
        class_strings = [cls_temp.build_class_string() for cls_temp in self.classes]
        result_string = '\n\n'.join(class_strings)
        return result_string

    def build_classes(self, class_name: str, json_data: dict):
        result_class = ClassTemplate(class_name)
        for key, value in json_data.items():
            if type(value) == dict:
                cls_name = to_camel_case(key)
                self.build_classes(cls_name, value)
                result_class.class_fields.append(FieldTemplate(key, cls_name, key))
            elif type(value) == list:
                list_element = value[0]
                if type(list_element) == dict:
                    cls_name = to_camel_case(key)
                    self.build_classes(cls_name, list_element)
                    result_class.class_fields.append(FieldTemplate(key, f'List[{cls_name}]', key))
                else:
                    result_class.class_fields.append(FieldTemplate(key, f'List[{type(value).__qualname__}]', key))
            else:
                result_class.class_fields.append(FieldTemplate(key, type(value).__qualname__, key))
        self.classes.append(result_class)