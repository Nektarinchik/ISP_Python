import json
import types
import dis
import inspect
import math

from factory import SerializerFactory
from types_deserializers import JsonTypesDeserializer
from serializer_types import SerializerTypes


class Vehicle:
    pass


class Car(Vehicle):

    def __init__(self, name, engine):
        self.__name = name
        self.__engine = engine
        self.__model = 'W210'

    def ride(self):
        print(f'{self.__name} is riding now')

    def get_info(self):
        print(f'name: {self.__name}')
        self.__engine.get_info()
        print(f'model: {self.__model}')

    def __hidden(self, name):
        print(name)


class Engine:

    def __init__(self, capacity):
        self.__capacity = capacity

    def get_info(self):
        print(f'capacity: {self.__capacity}')

gl = 10

def inc(x=1):

    global gl
    res = gl + 1
    f(1,9)

    print(res)


def f():

    def a(x):
        print(x)

    a(1)


def a():
    c()


def c():
    a()


def fib(n):

    if n == 1:

        return 1

    if n == 0:

        return 1

    return fib(n-1)+fib(n-2)

def test_func_with_kwargs(a,b,c,**kwargs):
    print(a,b,c)
    res = kwargs['indent']
    print(res)


if __name__ == '__main__':
    json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
    engine1 = Engine(2)
    car1 = Car('bmw', engine1)
    Car.f = f
    # print(isinstance(car1.f, types.MethodType))
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

    list2 = [
        ['s[tr1',1,23],3
    ]

    dict1 = {
        'dict1':{
            'st[r1': {
                'ke1': {
                    'one':  1
                }
            },
            'str2': 'str',
            'str3': 3,
            'str4': 4.2,
            'str5': 'str5',
            2:4,
            2:'str',
            2:[]
        }
    }

    with open('test.json', 'w') as f_obj:
        json_serializer.dump(a, f_obj)

    # with open('test.json', 'r') as f_obj:
    #     res = f_obj.read()
    #
    #     res = json_serializer.loads(res)
    #     print(res(7))

    # args = (None,None, None)
    # test_func_with_kwargs(*args)
    # print(Engine.__dict__['__init__'].__code__.co_kwonlyargcount)
