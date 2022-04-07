import json
import types
import dis

from factory import SerializerFactory
from serializer_types import SerializerTypes


class Vehicle:
    pass


class Car(Vehicle):

    def __init__(self, name, engine):
        self.__name = name
        self.__engine = engine

    def ride(self):
        print(f'"{self.__name} is riding now"')

    def __hidden(self, name):
        print(name)


class Engine:

    def __init__(self, capacity):
        self.__capacity = capacity


def inc(x: int):
    res = x + 1

    return res


if __name__ == '__main__':
    json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
    engine1 = Engine(2)
    car1 = Car('bmw', engine1)
    # dict1 = {
    #     'float': 1.4568,
    #     1.4568: 'float',
    #     'int': 789,
    #     789: 'int',
    #     'list': [
    #         1,
    #         2,
    #         456.2,
    #         'end_list'
    #     ],
    #     'tuple': (
    #         1,
    #         2,
    #         456.2,
    #         'end_tuple'
    #     ),
    #     'bool': True,
    #     'None': None,
    # }

    # print(json_serializer.dumps(inc))
    # print(json.dumps(dict1, indent=2))
    # with open('car1.json', 'w') as f_obj:
    #     json_serializer.dump(car1, f_obj)
    #
    # with open('car1.json', 'r') as f_obj:
    #     res = f_obj.read()
    #     print(type(eval(res)))

    list1 = [
        [
            'str1',
            'str2',
            2,
            3
        ],
        True,
        [
            'str1.1',
            23,
            'str2.2'
        ]
    ]
    with open('car1.json', 'w') as f_obj:
        json_serializer.dump(list1, f_obj)

    with open('car1.json', 'r') as f_obj:
        res = f_obj.read()

        print(json_serializer.loads(res))
