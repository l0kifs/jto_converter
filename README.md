# JTO Converter

## Description
Convert json object to dataclass and vice versa.
This package also provides tool for converting json object to dataclass template.

## Requirements
### Required structure of dataclass field
```python
field_name: Optional[FieldType] = field(default=Undefined, metadata={'name': 'json_field_name', 'required': False, 'validate': validate_function})
```
- `field_name` **[required]** can be any variable name.
-  `Optional` **[optional]** indicates that the field is nullable.
- `FieldType` **[required]** should be strongly typed.   
For example in case of field containing the list it should look like this `List[SomeClass]`
- `default` **[required]** sets default field's value. Set to `Undefined` by default.
- `name` **[required]** is the name of the field in original json.
- `required` **[required]** marked `True` if the field is required in the provided json.
- `validate` **[optional]** is the function that validates the field's value.
Validate function supports fields with simple types like `str`, `int`, `float`, `bool` and `List` of simple types.
The function has one argument - field's value. It should return `True` if the value is valid and `False` otherwise. 
Example lambda function: `lambda x: x > 0`

### Additional rules
- If dataclass field value set to `Undefined` then it will not be converted to json field
- If dataclass field type is not `Optional`
then all dataclass fields with `None` values will not be converted to json fields

## Examples

Convert json object to class objects
```python
from dataclasses import dataclass, field
from typing import List, Optional

from jto import JTOConverter
from jto.undefined_field import Undefined

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
    f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

@dataclass
class Data:
    first: Optional[str] = field(default=Undefined, metadata={'name': 'first', 'required': False, 'validate': lambda x: x == 'qwer'})
    last: Optional[str] = field(default=Undefined, metadata={'name': 'last', 'required': False})
    test: Optional[List[Test]] = field(default=Undefined, metadata={'name': 'test', 'required': False})

@dataclass
class Response:
    status: Optional[int] = field(default=Undefined, metadata={'name': 'status', 'required': False})
    data: Optional[Data] = field(default=Undefined, metadata={'name': 'data', 'required': False})


dataclass_object = JTOConverter.from_json(Response, data)
print(dataclass_object)

dataclass_object.status = None
json_object = JTOConverter.to_json(dataclass_object)
print(json_object)
```
Get class templates from json object

```python
from jto.dataclass_generator import DataclassGenerator

data = {
    "status": 200,
    "data": {
        "first": "foo",
        "last": "bar",
        "struct": [
            {"f1": "1"},
            {"f1": "2"}
        ]
    }
}

classes = DataclassGenerator()
classes_str = classes.build_classes_string('Response', data)
print(classes_str)
```
