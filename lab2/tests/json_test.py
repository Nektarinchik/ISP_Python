import objects_for_testing

from factory import SerializerFactory
from serializer_types import SerializerTypes
from unittest import TestCase, main


class JsonTest(TestCase):

    def setUp(self):
        self.json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
        self.filename = 'buff.json'

    def test_function(self):

        with open(self.filename, 'w') as f_obj:
            self.json_serializer.dump(objects_for_testing.func_with_builtin_func, f_obj)

        with open(self.filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        non_sorted_list = [9, 8, 7, 14, 28, 2, 3]
        sorted_list = res(non_sorted_list)
        non_sorted_list.sort()
        self.assertEqual(sorted_list, non_sorted_list)

    def test_function_with_function_from_other_package(self):

        with open(self.filename, 'w') as f_obj:
            self.json_serializer.dump(
                objects_for_testing.function_with_function_from_math,
                f_obj
            )

        with open(self.filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        print(res.__globals__)

        for i in range(1, 5):
            self.assertEqual(
                res(i),
                objects_for_testing.function_with_function_from_math(i)
            )

    def test_recursive_function(self):

        with open(self.filename, 'w') as f_obj:
            self.json_serializer.dump(objects_for_testing.fib, f_obj)

        with open(self.filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 10):
            self.assertEqual(objects_for_testing.fib(i), res(i))

    def test_lambda_function(self):
        func = lambda x, y: x * y

        with open(self.filename, 'w') as f_obj:
            self.json_serializer.dump(func, f_obj)

        with open(self.filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 15):
            self.assertEqual(func(i, i + 5), res(i, i + 5))

    def test_function_with_closure(self):

        with open(self.filename, 'w') as f_obj:
            self.json_serializer.dump(objects_for_testing.func_with_closure, f_obj)

        with open(self.filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 20):
            self.assertEqual(res(i), objects_for_testing.func_with_closure(i))

    def test_class_instance(self):

        engine = objects_for_testing.Engine(3)
        car = objects_for_testing.Car(
            'red',
            1980.0,
            10,
            2007,
            10000,
            'Mercedes',
            'W211',
            engine
        )
        with open(self.filename, 'w') as f_obj:
            self.json_serializer.dump(car, f_obj)

        with open(self.filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        print(res.__eq__(car))

        # self.assertEqual(res, engine)



if __name__ == '__main__':
    main()