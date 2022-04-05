import json

from factory import SerializerFactory
from serializer_types import SerializerTypes


def inc(x: int):
    res = x + 1

    return res


if __name__ == '__main__':
    json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
    json_serializer.dump(inc, 'haha')
    print('_______________________________________________')
    dict1 = {
        'key1': 'val1',
        'key2': []
    }

