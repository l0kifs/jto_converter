from dataclasses import dataclass, field

import pytest

from jto import JTOConverter
from jto.undefined_field import Undefined


def test_validate_simple_value():
    data = {"f1": "f1"}

    @dataclass
    class Test:
        f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                     'validate': lambda x: x == 'f1'})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1='f1')

    json_object = JTOConverter.to_json(dataclass_object)
    assert json_object == data


def test_validate_simple_value_fail():
    data = {"f1": "f1"}

    @dataclass
    class Test:
        f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                     'validate': lambda x: x == 'f2'})

    with pytest.raises(ValueError, match='Value "f1" of field "f1" is not valid'):
        JTOConverter.from_json(Test, data)


def test_validate_list_value():
    data = {"f1": ["f1", "f2"]}

    @dataclass
    class Test:
        f1: list = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                      'validate': lambda x: len(x) == 2})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1=["f1", "f2"])

    json_object = JTOConverter.to_json(dataclass_object)
    assert json_object == data


def test_validate_list_value_fail():
    data = {"f1": ["f1", "f2"]}

    @dataclass
    class Test:
        f1: list = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                      'validate': lambda x: len(x) == 3})

    with pytest.raises(ValueError, match=r'Value .* of field "f1" is not valid'):
        JTOConverter.from_json(Test, data)


def test_validate_dict_value():
    data = {"f1": {"f2": "f2"}}

    @dataclass
    class Test:
        f1: dict = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                      'validate': lambda x: x['f2'] == 'f2'})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1={"f2": "f2"})

    json_object = JTOConverter.to_json(dataclass_object)
    assert json_object == data


def test_validate_dict_value_fail():
    data = {"f1": {"f2": "f2"}}

    @dataclass
    class Test:
        f1: dict = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                      'validate': lambda x: x['f2'] == 'f3'})

    with pytest.raises(ValueError, match=r'Value .* of field "f1" is not valid'):
        JTOConverter.from_json(Test, data)


def test_validate_dataclass_value():
    data = {"f1": {"f2": "f2"}}

    @dataclass
    class Test2:
        f2: str = field(default=Undefined, metadata={'name': 'f2', 'required': False})

    @dataclass
    class Test:
        f1: Test2 = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                       'validate': lambda x: x == 'nothing'})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1=Test2(f2='f2'))

    json_object = JTOConverter.to_json(dataclass_object)
    assert json_object == data


def test_validate_is_not_callable():
    data = {"f1": "f1"}

    @dataclass
    class Test:
        f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': False,
                                                     'validate': 'not callable'})

    with pytest.raises(ValueError, match='Value of metadata key "validate" is not callable'):
        JTOConverter.from_json(Test, data)
