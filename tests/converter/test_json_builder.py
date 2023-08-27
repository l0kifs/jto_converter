from dataclasses import dataclass, field
from typing import Optional, List

import pytest

from jto import JTOConverter
from jto.undefined_field import Undefined


def test_nullable_field():
    @dataclass
    class Test:
        f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    test_obj = Test(f1=None)
    expected_json = {"f1": None}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_not_nullable_field():
    @dataclass
    class Test:
        f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    test_obj = Test(f1=None)
    expected_json = {}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_undefined_field():
    @dataclass
    class Test:
        f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    test_obj = Test()
    expected_json = {}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_dataclass_field():
    @dataclass
    class Test2:
        f2: str = field(default=Undefined, metadata={'name': 'f2', 'required': True})

    @dataclass
    class Test:
        f1: Test2 = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    test_obj = Test(f1=Test2(f2='test'))
    expected_json = {"f1": {"f2": "test"}}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_list_of_dataclasses_field():
    @dataclass
    class Test2:
        f2: str = field(default=Undefined, metadata={'name': 'f2', 'required': True})

    @dataclass
    class Test:
        f1: List[Test2] = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    test_obj = Test(f1=[Test2(f2='test')])
    expected_json = {"f1": [{"f2": "test"}]}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_list_of_dataclasses_field_with_nullable():
    @dataclass
    class Test2:
        f2: Optional[str] = field(default=Undefined, metadata={'name': 'f2', 'required': False})

    @dataclass
    class Test:
        f1: List[Test2] = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    test_obj = Test(f1=[Test2(f2=None), Test2(f2='test')])
    expected_json = {"f1": [{"f2": None}, {"f2": "test"}]}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_list_of_dataclasses_field_with_undefined():
    @dataclass
    class Test2:
        f2: Optional[str] = field(default=Undefined, metadata={'name': 'f2', 'required': False})

    @dataclass
    class Test:
        f1: List[Test2] = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    test_obj = Test(f1=[Test2(f2=Undefined)])
    expected_json = {"f1": [{}]}

    json_object = JTOConverter.to_json(test_obj)
    assert json_object == expected_json


def test_dataclass_obj_is_not_dataclass():
    with pytest.raises(TypeError):
        JTOConverter.to_json('test')
