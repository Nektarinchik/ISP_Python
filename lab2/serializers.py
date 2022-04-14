import abc
import inspect
import typing

import toml
import tomli
import types
import _io
import yaml

import json_types_deserializer
import json_types_serializer
import yaml_toml_types_deserializer
import yaml_toml_types_serializer

from exceptions import JSONDecodeError
from exceptions import YAMLDecodeError


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
                res = json_types_serializer.JsonTypesSerializer.user_def_function_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, types.LambdaType):
                res = json_types_serializer.JsonTypesSerializer.lambda_function_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, types.BuiltinFunctionType):
                res = json_types_serializer.JsonTypesSerializer.builtin_function_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, int):
                temp = json_types_serializer.JsonTypesSerializer.int_serializer(
                    obj
                )
                res = temp

            elif isinstance(obj, float):
                temp = json_types_serializer.JsonTypesSerializer.float_serializer(
                    obj
                )
                res = temp

            elif isinstance(obj, str):
                res = f'"{obj}"'

            elif isinstance(obj, list):
                res = json_types_serializer.JsonTypesSerializer.list_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, dict):
                res = json_types_serializer.JsonTypesSerializer.dict_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, tuple):
                res = json_types_serializer.JsonTypesSerializer.tuple_serializer(
                    obj,
                    indent=indent
                )

            elif isinstance(obj, bool):
                temp = json_types_serializer.JsonTypesSerializer.bool_serializer(
                    obj
                )
                res = temp

            elif isinstance(obj, types.NoneType):
                temp = json_types_serializer.JsonTypesSerializer.none_serializer()
                res = temp

            elif inspect.isclass(obj):
                res = json_types_serializer.JsonTypesSerializer.class_serializer(
                    obj,
                    indent=indent
                )

            elif inspect.isclass(type(obj)):
                res = json_types_serializer.JsonTypesSerializer.class_instance_serializer(
                    obj,
                    indent=indent
                )

            elif inspect.iscode(obj):
                res = json_types_serializer.JsonTypesSerializer.code_object_serializer(
                    obj,
                    indent=indent
                )

            else:
                raise TypeError(f'Object of {type(obj)} is not JSON serializable')

        except TypeError as err:
            print(err)

        finally:

            if not res:
                res = json_types_serializer.JsonTypesSerializer.none_serializer()

            return res

    def load(self, f_obj: _io.TextIOWrapper):
        buff = f_obj.read()
        res = self.loads(buff)

        return res

    def loads(self, s: str):

        try:

            res = json_types_deserializer.JsonTypesDeserializer.json_string_deserializer(s)

            return res

        except JSONDecodeError as err:

            print(err)
            raise SystemExit(1)


class YamlSerializer(Serializer):

    def dump(self, obj, f_obj: _io.TextIOWrapper, indent=2):
        res = yaml_toml_types_serializer.YamlTomlTypesSerializer.get_type(obj)
        yaml.dump(res, f_obj, indent=indent)

    def dumps(self, obj) -> str:
        res = yaml_toml_types_serializer.YamlTomlTypesSerializer.get_type(obj)
        res = yaml.dump(res)

        return res

    def load(self, f_obj: _io.TextIOWrapper):
        buff = yaml.unsafe_load(f_obj)

        try:
            res = yaml_toml_types_deserializer.YamlTomlTypesDeserializer.get_type(buff)

        except YAMLDecodeError as err:
            print(err)

            return None

        return res

    def loads(self, s: str):
        buff = yaml.unsafe_load(s)

        try:
            res = yaml_toml_types_deserializer.YamlTomlTypesDeserializer.get_type(buff)

        except YAMLDecodeError as err:
            print(err)

            return None

        return res


class TomlSerializer(Serializer):

    def dump(self, obj, f_obj: _io.TextIOWrapper, indent=2):
        res = yaml_toml_types_serializer.YamlTomlTypesSerializer.get_type(obj)
        toml.dump(res, f_obj)

    def dumps(self, obj, indent=2) -> str:
        res = yaml_toml_types_serializer.YamlTomlTypesSerializer.get_type(obj)
        res = toml.dumps(res)

        return res

    def load(self, f_obj: typing.BinaryIO):
        """needed binary file object for reading"""
        buff = tomli.load(f_obj)

        try:
            res = yaml_toml_types_deserializer.YamlTomlTypesDeserializer.get_type(buff)

        except YAMLDecodeError as err:
            print(err)

            return None

        return res

    def loads(self, s: str):
        """needed binary file object for reading"""
        buff = tomli.loads(s)

        try:
            res = yaml_toml_types_deserializer.YamlTomlTypesDeserializer.get_type(buff)

        except YAMLDecodeError as err:
            print(err)

            return None

        return res
