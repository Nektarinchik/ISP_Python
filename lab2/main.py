from tests import objects_for_testing
from factory import SerializerFactory
from serializer_types import SerializerTypes

from tests import objects_for_testing

if __name__ == '__main__':
    yaml_serializer = SerializerFactory.create_serializer(SerializerTypes.yaml)
    json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
    toml_serializer = SerializerFactory.create_serializer(SerializerTypes.toml)

    dict1 = {
        'str1': 1,
        'str2': 2,
        'str3': 3
    }
    # with open('test.json', 'w') as f_obj:
    #     json_serializer.dump(sorted, f_obj)
    with open('test.toml', 'w') as f_obj:
        toml_serializer.dump(objects_for_testing.Car, f_obj)

    with open('test.toml', 'rb') as f_obj:
        res = toml_serializer.load(f_obj)
        print(res.__dict__)

    print('Hello')
