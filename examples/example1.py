from dataclasses import dataclass, field
from typing import List

from jto import JTOConverter

data = {
    "status": 200,
    "data": {
        "first": "qwer",
        "last": "qwer",
        "test": [
            {"f1": "1"},
            {"f1": "2"}
        ]
    }
}


@dataclass
class Test:
    f1: str = field(default=None, metadata={'name': 'f1', 'required': False})


@dataclass
class Data:
    first: str = field(default=None, metadata={'name': 'first', 'required': False})
    last: str = field(default=None, metadata={'name': 'last', 'required': False})
    test: List[Test] = field(default=None, metadata={'name': 'test', 'required': False})


@dataclass
class Response:
    status: int = field(default=None, metadata={'name': 'status', 'required': False})
    data: Data = field(default=None, metadata={'name': 'data', 'required': False})


dataclass_object = JTOConverter.from_json(Response, data)
print(dataclass_object)

dataclass_object.status = None
json_object = JTOConverter.to_json(dataclass_object, drop_empty_keys=True)
print(json_object)
