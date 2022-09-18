from jto.dataclass_generator import ClassesTemplate

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

classes = ClassesTemplate()
classes.build_classes('Response', data)
print(classes)

classes_str = classes.build_classes_string()
print(classes_str)
