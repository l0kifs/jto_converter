from jto.dataclass_generator import ClassesTemplate, FieldTemplate

from src.jto.dataclass_generator import ClassTemplate


def test_parse_empty_dict():
    data = {}

    test_classes = ClassesTemplate()
    test_classes.build_classes('Response', data)
    expected_classes = ClassesTemplate(classes=[ClassTemplate(class_name='Response', class_fields=[])])
    assert str(test_classes) == str(expected_classes)

    classes_str = test_classes.build_classes_string()
    assert classes_str == "@dataclass\nclass Response:\n    "


def test_empty_list_value():
    data = {'var': []}

    test_classes = ClassesTemplate()
    test_classes.build_classes('Response', data)
    expected_classes = ClassesTemplate(classes=[
        ClassTemplate(class_name='Response', class_fields=[
            FieldTemplate(field_name='var', field_type="List[<class 'object'>]",
                          json_field_name='var', default_value=None, required=False)
        ])
    ])
    assert str(test_classes) == str(expected_classes)

    classes_str = test_classes.build_classes_string()
    assert classes_str == "@dataclass\nclass Response:\n    var: List[<class 'object'>] = " \
                          "field(default=None, metadata={'name': 'var', 'required': False})"
