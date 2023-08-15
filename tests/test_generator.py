from jto.dataclass_generator import ClassesTemplate, FieldTemplate, ClassTemplate
from jto.undefined_field import Undefined


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
                          json_field_name='var', default_value=Undefined.__name__, required=False)
        ])
    ])
    assert str(test_classes) == str(expected_classes)

    classes_str = test_classes.build_classes_string()
    assert classes_str == "@dataclass\nclass Response:\n    var: Optional[List[<class 'object'>]] = " \
                          "field(default=Undefined, metadata={'name': 'var', 'required': False})"
