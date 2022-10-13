from dataclasses import dataclass, field

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


