import abc
import types

import types_serializers


class Serializer:

    @abc.abstractmethod
    def dump(self, obj, fp, indent=2):
        """Method that serialize Python object into the file"""

    @abc.abstractmethod
    def dumps(self, obj, indent=2) -> str:
        """Method that serialize Python object into the string"""

    @abc.abstractmethod
    def load(self, fp):
        """Method that deserialize Python object from file"""

    @abc.abstractmethod
    def loads(self, s):
        """Method that deserialize Python object from string"""


class JsonSerializer(Serializer):

    def dump(self, obj, fp, indent=2):

        if isinstance(obj, types.FunctionType):
            res_str = types_serializers.JsonTypesSerializer.user_def_function_serializer(
                obj,
                indent=indent
            )
            print(res_str)

    def dumps(self, obj, indent=2) -> str:
        pass

    def load(self, fp):
        pass

    def loads(self, s):
        pass


class YamlSerializer(Serializer):

    def dump(self, obj, fp, indent=2):
        pass

    def dumps(self, obj, indent=2) -> str:
        pass

    def load(self, fp):
        pass

    def loads(self, s):
        pass


class TomlSerializer(Serializer):

    def dump(self, obj, fp, indent=2):
        pass

    def dumps(self, obj, indent=2) -> str:
        pass

    def load(self, fp):
        pass

    def loads(self, s):
        pass
