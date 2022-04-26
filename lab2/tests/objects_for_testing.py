import math


class Engine:

    def __init__(self, engine_capacity):
        self.__engine_capacity = engine_capacity

    def __eq__(self, other):
        if self.__engine_capacity == other.__engine_capacity:
            return True

        return False

    def get_info(self):
        print(f'Engine capacity: {self.__engine_capacity}')


class Car:

    def __init__(self,
                 color: str,
                 weight: float,
                 fuel_consumption: float,
                 year_of_release: int,
                 price: int,
                 name: str,
                 model: str,
                 engine: Engine):
        self.__color = color
        self.__weight = weight
        self.__fuel_consumption = fuel_consumption
        self.__year_of_release = year_of_release
        self.__price = price
        self.__name = name
        self.__model = model
        self.__engine = engine

    def __eq__(self, other):
        if self.__color == other.__color \
                and self.__weight == other.__weight \
                and self.__fuel_consumption == other.__fuel_consumption \
                and self.__year_of_release == other.__year_of_release \
                and self.__price == other.__price \
                and self.__name == other.__name \
                and self.__model == other.__model \
                and self.__engine == other.__engine:
            return True

        return False

    def get_info(self):
        print(f'Color: {self.__color}')
        print(f'Weight: {self.__weight}')
        print(f'Fuel consumption: {self.__fuel_consumption}')
        print(f'Price: {self.__price}')
        print(f'Name: {self.__name}')
        print(f'Model: {self.__model}')
        self.__engine.get_info()

    def ride(self):
        print(f'{self.__name} {self.__model} is riding now!')


def func_with_builtin_func(arr: list):
    res = sorted(arr)

    return res


def fib(n: int):
    if n == 1:
        return 1

    if n == 0:
        return 1

    return fib(n - 1) + fib(n - 2)


mes = 'Hello'


def func_with_closure(x: int):
    global mes
    print(mes)

    def increase_value(interval: int):
        res = x + interval

        return res

    return increase_value(5)


def function_with_function_from_math(x):
    sin = math.sin(x)
    print(sin)

    return sin

c = 2
def f(x, y):
    global c
    return math.sin(x * y * c)
