from tests import objects_for_testing
from serializers import serializers

from factory.factory import SerializerFactory
from factory.serializer_types import SerializerTypes


if __name__ == '__main__':

    json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
    yaml_serializer = SerializerFactory.create_serializer(SerializerTypes.yaml)

    with open('test.yaml', 'w') as f_obj:
        yaml_serializer.dump(objects_for_testing.func_with_closure, f_obj)

    with open('test.yaml', 'r') as f_obj:
        res = yaml_serializer.load(f_obj)




