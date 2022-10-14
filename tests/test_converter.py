from dataclasses import dataclass, field

import pytest
from jto import JTOConverter


def test_convert_empty_dict():
    data = {}

    @dataclass
    class Test:
        f1: str = field(default=None, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test()

    json_object = JTOConverter.to_json(dataclass_object, drop_empty_keys=True)
    assert json_object == {}


def test_convert_dict_with_unexpected_values():
    data = {"one": 1}

    @dataclass
    class Test:
        f1: str = field(default=None, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test()


def test_convert_value_with_unexpected_type():
    data = {"f1": 1}

    @dataclass
    class Test:
        f1: str = field(default=None, metadata={'name': 'f1', 'required': False})

    with pytest.raises(TypeError, match="Expected value type is <class 'str'>, but received <class 'int'>"):
        JTOConverter.from_json(Test, data)
