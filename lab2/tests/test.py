import objects_for_testing

from factory import SerializerFactory
from serializer_types import SerializerTypes
from unittest import TestCase, main


class SerializerTest(TestCase):

    def setUp(self):
        self.json_serializer = SerializerFactory.create_serializer(SerializerTypes.json)
        self.yaml_serializer = SerializerFactory.create_serializer(SerializerTypes.yaml)
        self.toml_serializer = SerializerFactory.create_serializer(SerializerTypes.toml)
        self.json_filename = 'buff.json'
        self.yaml_filename = 'buff.yaml'
        self.toml_filename = 'buff.toml'

    def test_function(self):
        """
        Testing serialization of function with builtin function inside
        """

        """JSON test"""
        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(objects_for_testing.func_with_builtin_func, f_obj)

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        non_sorted_list = [9, 8, 7, 14, 28, 2, 3]
        sorted_list = res(non_sorted_list)
        non_sorted_list.sort()
        self.assertEqual(sorted_list, non_sorted_list)

        """YAML test"""
        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(objects_for_testing.func_with_builtin_func, f_obj)

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

        non_sorted_list = [9, 8, 7, 14, 28, 2, 3]
        sorted_list = res(non_sorted_list)
        non_sorted_list.sort()
        self.assertEqual(sorted_list, non_sorted_list)

        """TOML test"""
        with open(self.toml_filename, 'w') as f_obj:
            self.toml_serializer.dump(objects_for_testing.func_with_builtin_func, f_obj)

        with open(self.toml_filename, 'rb') as f_obj:
            res = self.toml_serializer.load(f_obj)

        non_sorted_list = [9, 8, 7, 14, 28, 2, 3]
        sorted_list = res(non_sorted_list)
        non_sorted_list.sort()
        self.assertEqual(sorted_list, non_sorted_list)

    def test_function_with_function_from_other_package(self):
        """
        Testing serialization with function from other package inside
        """

        """JSON test"""
        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(
                objects_for_testing.function_with_function_from_math,
                f_obj
            )

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 5):
            self.assertEqual(
                res(i),
                objects_for_testing.function_with_function_from_math(i)
            )

        """YAML test"""
        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(
                objects_for_testing.function_with_function_from_math,
                f_obj
            )

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

        for i in range(1, 5):
            self.assertEqual(
                res(i),
                objects_for_testing.function_with_function_from_math(i)
            )

        """TOML test"""
        with open(self.toml_filename, 'w') as f_obj:
            self.toml_serializer.dump(
                objects_for_testing.function_with_function_from_math,
                f_obj
            )

        with open(self.toml_filename, 'rb') as f_obj:
            res = self.toml_serializer.load(f_obj)

        for i in range(1, 5):
            self.assertEqual(
                res(i),
                objects_for_testing.function_with_function_from_math(i)
            )

    def test_recursive_function(self):
        """
        Testing of recursive function that store itself in __globals__ attr
        """

        """JSON test"""
        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(objects_for_testing.fib, f_obj)

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 10):
            self.assertEqual(objects_for_testing.fib(i), res(i))

        """YAML test"""
        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(objects_for_testing.fib, f_obj)

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

        for i in range(1, 10):
            self.assertEqual(objects_for_testing.fib(i), res(i))

        """TOML test"""
        with open(self.toml_filename, 'w') as f_obj:
            self.toml_serializer.dump(objects_for_testing.fib, f_obj)

        with open(self.toml_filename, 'rb') as f_obj:
            res = self.toml_serializer.load(f_obj)

        for i in range(1, 10):
            self.assertEqual(objects_for_testing.fib(i), res(i))

    def test_lambda_function(self):
        """Testing serialization of function defined like lambda"""

        """JSON test"""
        func = lambda x, y: x * y

        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(func, f_obj)

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 15):
            self.assertEqual(func(i, i + 5), res(i, i + 5))

        """YAML test"""
        func = lambda x, y: x * y

        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(func, f_obj)

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

        for i in range(1, 15):
            self.assertEqual(func(i, i + 5), res(i, i + 5))

        """TOML test"""
        func = lambda x, y: x * y

        with open(self.toml_filename, 'w') as f_obj:
            self.toml_serializer.dump(func, f_obj)

        with open(self.toml_filename, 'rb') as f_obj:
            res = self.toml_serializer.load(f_obj)

        for i in range(1, 15):
            self.assertEqual(func(i, i + 5), res(i, i + 5))

    def test_function_with_closure(self):
        """Testing serialization of closures"""

        """JSON test"""
        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(objects_for_testing.func_with_closure, f_obj)

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        for i in range(1, 20):
            self.assertEqual(res(i), objects_for_testing.func_with_closure(i))

        """YAML test"""
        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(objects_for_testing.func_with_closure, f_obj)

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

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

        """JSON test"""
        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(car, f_obj)

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        self.assertEqual(res, car)

        """YAML test"""
        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(car, f_obj)

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

        self.assertEqual(res, car)

        """TOML serializer"""
        with open(self.toml_filename, 'w') as f_obj:
            self.toml_serializer.dump(car, f_obj)

        with open(self.toml_filename, 'rb') as f_obj:
            res = self.toml_serializer.load(f_obj)

        self.assertEqual(res, car)

    def test_exception(self):
        dict1 = {
            'str1': 1,
            'str2': 2,
            'str3': 3,
            'str4': 4
        }
        with open(self.json_filename, 'w') as f_obj:
            f_obj.write('}')

        with open(self.json_filename, 'a') as f_obj:
            self.json_serializer.dump(dict1, f_obj)

        with open(self.json_filename, 'r') as f_obj:

            with self.assertRaises(SystemExit) as context:
                res = self.json_serializer.load(f_obj)
                print(res)

            self.assertEqual(context.exception.code, 1)

    def test_primitive_type(self):
        test_dict = {
            'list': [
                1.1,
                2,
                {
                    's{tr1': 1,
                    'str2': None
                },
                [
                    None,
                    'str3'
                ]
            ],
            'dict': {
                'str1': 1,
                'str2': 2.2,
                'empty_list': []
            },
            'end_dict': None
        }

        """JSON test"""
        with open(self.json_filename, 'w') as f_obj:
            self.json_serializer.dump(test_dict, f_obj)

        with open(self.json_filename, 'r') as f_obj:
            res = self.json_serializer.load(f_obj)

        self.assertEqual(test_dict, res)

        """YAML test"""
        with open(self.yaml_filename, 'w') as f_obj:
            self.yaml_serializer.dump(test_dict, f_obj)

        with open(self.yaml_filename, 'r') as f_obj:
            res = self.yaml_serializer.load(f_obj)

        self.assertEqual(test_dict, res)


if __name__ == '__main__':
    main()
