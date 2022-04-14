import builtins
import types

from exceptions import YAMLDecodeError


class YamlTomlTypesDeserializer:

    @staticmethod
    def get_type(obj) -> object:

        if isinstance(obj, int) or \
                isinstance(obj, float) or \
                isinstance(obj, bool) or \
                isinstance(obj, types.NoneType):

            return obj

        elif isinstance(obj, str):

            if obj == 'None':
                return None

            return obj

        elif isinstance(obj, dict):

            try:
                res = YamlTomlTypesDeserializer.dict_deserializer(obj)

            except TypeError as err:
                print(err)

                raise SystemExit(1)

            return res

        elif isinstance(obj, list):
            res = YamlTomlTypesDeserializer.list_deserializer(obj)

            return res

        elif isinstance(obj, tuple):
            res = YamlTomlTypesDeserializer.tuple_deserializer(obj)

            return res

        else:

            raise YAMLDecodeError('incorrect YAML format')

    @staticmethod
    def dict_deserializer(obj: dict) -> object:
        buff = YamlTomlTypesDeserializer.get_python_type_from_object(obj)

        deserialized_dict = {}
        if isinstance(buff, dict):

            key_buff, value_buff = None, None
            for key, value in obj.items():

                """determine the key type"""
                if isinstance(key, int) or \
                        isinstance(key, float) or \
                        isinstance(key, str) or \
                        isinstance(key, bool) or \
                        isinstance(key, types.NoneType):
                    key_buff = key

                else:

                    raise TypeError(f'keys must be str, int, float, bool or None, not {type(key)}')

                """determine the value type"""
                try:
                    value_buff = YamlTomlTypesDeserializer.get_type(value)

                except YAMLDecodeError as err:
                    print(err)

                    raise SystemExit(1)

                deserialized_dict[key_buff] = value_buff

            return deserialized_dict

        else:

            return buff

    @staticmethod
    def list_deserializer(obj: list) -> list:

        deserialized_list = []
        for item in obj:

            try:
                buff = YamlTomlTypesDeserializer.get_type(item)

            except YAMLDecodeError as err:
                print(err)

                raise SystemExit(1)

            deserialized_list.append(buff)

        return deserialized_list

    @staticmethod
    def tuple_deserializer(obj: tuple) -> tuple:
        res = YamlTomlTypesDeserializer.list_deserializer(list(obj))

        return tuple(res)

    @staticmethod
    def get_python_type_from_object(obj: dict):

        try:

            type = obj['type']

            if type == 'ClassType':
                res = YamlTomlTypesDeserializer.get_class_from_dict(obj)

                return res

            elif type == 'FunctionType':
                res = YamlTomlTypesDeserializer.get_function_from_dict(obj)

                return res

            elif type == 'BuiltinFunctionType':
                res = YamlTomlTypesDeserializer.get_builtin_function_from_dict(obj)

                return res

            elif type == 'ClassInstanceType':
                res = YamlTomlTypesDeserializer.get_class_instance_form_dict(obj)

                return res

            elif type == 'CodeType':
                res = YamlTomlTypesDeserializer.get_code_object_from_dict(obj)

                return res

            else:

                return obj

        except KeyError:

            return obj

    @staticmethod
    def get_function_from_dict(obj: dict) -> types.FunctionType:
        is_recursive = False

        func_globs = {}
        serialized_globs = obj['__globals__']
        for key, value in serialized_globs.items():

            if value == 'recursive':  # it means that our function is recursive
                is_recursive = True

            elif isinstance(value, dict):
                temp = YamlTomlTypesDeserializer.get_python_type_from_object(value)

                func_globs[key] = temp

            elif isinstance(value, list):
                func_globs[key] = value

            elif isinstance(value, str):

                """this means that you need to connect the module"""
                if value == 'module':
                    func_globs[key] = __import__(key)
                    continue

                func_globs[key] = value

            elif isinstance(value, int):
                func_globs[key] = value

            elif isinstance(value, float):
                func_globs[key] = value

            elif isinstance(value, bool):
                func_globs[key] = value

            elif isinstance(value, types.NoneType):
                func_globs[key] = value

        func_code = YamlTomlTypesDeserializer.get_code_object_from_dict(obj['__code__'])

        func = types.FunctionType(func_code,
                                  func_globs,
                                  func_code.co_name
                                  )

        if is_recursive:  # if our function is recursive then we will store it in the globals
            func.__globals__[func.__name__] = func

        return func

    @staticmethod
    def get_class_from_dict(obj: dict) -> type:
        if obj['name'] == 'object':
            return object

        deserialized_bases = YamlTomlTypesDeserializer.list_deserializer(obj['bases'])

        buff = None
        namespace_deserialized = {}
        namespace_serialized = obj['type_definition']
        for name, attr in namespace_serialized.items():

            try:
                buff = YamlTomlTypesDeserializer.get_type(attr)

            except YAMLDecodeError as err:
                print(err)

                raise SystemExit(1)

            namespace_deserialized[name] = buff

        name = obj['name']
        new_cl = type(name, tuple(deserialized_bases), namespace_deserialized)

        return new_cl

    @staticmethod
    def get_builtin_function_from_dict(obj: dict) -> types.BuiltinFunctionType:
        name = obj['name']
        builtin_function_pair = dict(filter(lambda it: it[0] == name, vars(builtins).items()))
        builtin_function = builtin_function_pair[name]

        return builtin_function

    @staticmethod
    def get_class_instance_form_dict(obj: dict) -> object:
        object_class = YamlTomlTypesDeserializer.get_class_from_dict(obj['class_definition'])
        attrs_des = obj['object_definition']
        attrs = YamlTomlTypesDeserializer.dict_deserializer(attrs_des)
        #print(object_class.__dict__)
        init_args_count = object_class.__dict__['__init__'].__code__.co_argcount

        args = []
        for i in range(init_args_count - 1):
            args.append(None)

        class_instance = object_class(*args)

        for name, value in attrs.items():
            class_instance.__setattr__(name, value)

        return class_instance

    @staticmethod
    def get_code_object_from_dict(obj: dict) -> types.CodeType:

        def func():
            pass

        co_name = obj['co_name']
        co_filename = func.__code__.co_filename
        co_nlocals = obj['co_nlocals']
        co_argcount = obj['co_argcount']
        co_varnames = tuple(obj['co_varnames'])
        co_names = tuple(obj['co_names'])
        co_cellvars = tuple(obj['co_cellvars'])
        co_freevars = tuple(obj['co_freevars'])
        co_posonlyargcount = obj['co_posonlyargcount']
        co_kwonlyargcount = obj['co_kwonlyargcount']
        co_firstlineno = obj['co_firstlineno']
        co_lnotab = bytes(obj['co_lnotab'])
        co_stacksize = obj['co_stacksize']
        co_code = bytes(obj['co_code'])
        co_consts = tuple(YamlTomlTypesDeserializer.list_deserializer(obj['co_consts']))
        co_flags = obj['co_flags']

        code_obj = types.CodeType(
            co_argcount,
            co_posonlyargcount,
            co_kwonlyargcount,
            co_nlocals,
            co_stacksize,
            co_flags,
            co_code,
            co_consts,
            co_names,
            co_varnames,
            co_filename,
            co_name,
            co_firstlineno,
            co_lnotab,
            co_freevars,
            co_cellvars,
        )

        return code_obj
