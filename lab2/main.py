import json

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
    print(json_serializer.dump(Car, 'haha'))
    '''list1 = [1,{'d':1},(1,2)]
    print(json_serializer.dump(list1, 'haha'))'''

