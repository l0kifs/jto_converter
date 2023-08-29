from dataclasses import dataclass, field
from typing import Optional, List

import pytest

from jto import JTOConverter
from jto.undefined_field import Undefined


def test_simple_list_type():
    data = {
        "f1": [1, 2, 3]
    }

    @dataclass
    class Test:
        f1: list = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1=[1, 2, 3])


def test_simple_dict_type():
    data = {
        "f1": {"f2": 1}
    }

    @dataclass
    class Test:
        f1: dict = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1={"f2": 1})
