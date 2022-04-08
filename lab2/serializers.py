import _io
import abc
import inspect
import types

import types_serializers
import types_deserializers

from exceptions import JSONDecodeError


class Serializer:

    @abc.abstractmethod
    def dump(self, obj, f_obj: _io.TextIOWrapper, indent=2):
        """Method that serialize Python object into the file"""

    @abc.abstractmethod
    def dumps(self, obj, indent=2) -> str:
        """Method that serialize Python object into the string"""

    @abc.abstractmethod
    def load(self, f_obj: _io.TextIOWrapper):
        """Method that deserialize Python object from file"""

    @abc.abstractmethod
    def loads(self, s: str):
        """Method that deserialize Python object from string"""


class JsonSerializer(Serializer):

    def dump(self, obj, f_obj: _io.TextIOWrapper, indent=2):
        res = self.dumps(obj, indent=indent)

        f_obj.write(res)

    def dumps(self, obj, indent=2) -> str:

        try:

            res = ''
            if isinstance(obj, types.FunctionType):
                res = types_serializers.JsonTypesSerializer.user_def_function_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, types.LambdaType):
                res = types_serializers.JsonTypesSerializer.lambda_function_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, types.BuiltinFunctionType):
                res = types_serializers.JsonTypesSerializer.builtin_function_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, int):
                temp = types_serializers.JsonTypesSerializer.int_serializer(
                    obj
                )
                res = temp

            elif isinstance(obj, float):
                temp = types_serializers.JsonTypesSerializer.float_serializer(
                    obj
                )
                res = temp

            elif isinstance(obj, str):
                res = f'"{obj}"'

            elif isinstance(obj, list):
                res = types_serializers.JsonTypesSerializer.list_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, dict):
                res = types_serializers.JsonTypesSerializer.dict_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, tuple):
                res = types_serializers.JsonTypesSerializer.tuple_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, bool):
                temp = types_serializers.JsonTypesSerializer.bool_serializer(
                    obj
                )
                res = temp

            elif isinstance(obj, types.NoneType):
                temp = types_serializers.JsonTypesSerializer.none_serializer()
                res = temp

            elif inspect.isclass(obj):
                res = types_serializers.JsonTypesSerializer.class_serializer(
                    obj,
                    indent=indent
                )

            elif inspect.isclass(type(obj)):
                res = types_serializers.JsonTypesSerializer.class_instance_serializer(
                    obj,
                    indent=indent
                )

            else:
                raise TypeError(f'Object of {type(obj)} is not JSON serializable')

        except TypeError as err:
            print(err)

        finally:

            if not res:
                res = types_serializers.JsonTypesSerializer.none_serializer()

            return res

    def load(self, f_obj: _io.TextIOWrapper):
        pass

    def loads(self, s: str):

        try:

            res = types_deserializers.JsonTypesDeserializer.json_string_deserializer(s)

            return res

        except JSONDecodeError as err:

            print(err)
            raise SystemExit(1)


class YamlSerializer(Serializer):

    def dump(self, obj, f_obj: _io.TextIOWrapper, indent=2):
        pass

    def dumps(self, obj, indent=2) -> str:
        pass

    def load(self, f_obj: _io.TextIOWrapper):
        pass

    def loads(self, s: str):
        pass


class TomlSerializer(Serializer):

    def dump(self, obj, f_obj: _io.TextIOWrapper, indent=2):
        pass

    def dumps(self, obj, indent=2) -> str:
        pass

    def load(self, f_obj: _io.TextIOWrapper):
        pass

    def loads(self, s: str):
        pass
