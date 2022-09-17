# JTO Converter

## Description
Convert json object to dataclass and vice versa.  

## Requirements
### Required structure of dataclass field
All the parts of the below structure are required.
```python
field_name: str = field(default=None, metadata={'name': 'json_field_name', 'required': False})
```
- `field_name` can be any variable name.
- field type should be strongly typed.   
For example in case of field containing the list it should look like this `List[SomeClass]`
- `default` field's value in the most cases will be `None`, but it also can be changed.
- `name` is the name of the field in original json including.
- `required` marked `True` if the field is required in the provided json.
