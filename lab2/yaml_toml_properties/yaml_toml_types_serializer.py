import inspect
import types


class YamlTomlTypesSerializer:

    @staticmethod
    def get_type(obj):

        if isinstance(obj, int) or \
                isinstance(obj, float) or \
                isinstance(obj, str) or \
                isinstance(obj, bool) or \
                isinstance(obj, types.NoneType):
            res = obj

        elif isinstance(obj, types.FunctionType):
            res = YamlTomlTypesSerializer.user_def_function_serializer(
                obj
            )

        elif isinstance(obj, types.LambdaType):
            res = YamlTomlTypesSerializer.lambda_function_serializer(
                obj
            )

        elif isinstance(obj, types.BuiltinFunctionType):
            res = YamlTomlTypesSerializer.builtin_function_serializer(
                obj
            )

        elif isinstance(obj, types.MethodType):
            res = YamlTomlTypesSerializer.class_instance_method_serializer(obj)

        elif isinstance(obj, list):
            res = YamlTomlTypesSerializer.list_serializer(
                obj
            )

        elif isinstance(obj, dict):
            res = YamlTomlTypesSerializer.dict_serializer(
                obj
            )

        elif isinstance(obj, tuple):
            res = YamlTomlTypesSerializer.tuple_serializer(
                obj
            )

        elif isinstance(obj, types.ModuleType):
            res = 'module'

        elif inspect.isclass(obj):
            res = YamlTomlTypesSerializer.class_serializer(
                obj
            )

        elif inspect.iscode(obj):
            res = YamlTomlTypesSerializer.code_object_serializer(
                obj
            )

        elif inspect.isclass(type(obj)):
            res = YamlTomlTypesSerializer.class_instance_serializer(
                obj
            )

        else:

            raise TypeError(f'Object of {type(obj)} is not YAML serializable')

        return res

    @staticmethod
    def user_def_function_serializer(func: types.FunctionType) -> dict:
        func_obj = {}

        func_obj['type'] = 'FunctionType'

        """write necessary modules for working"""
        globs = YamlTomlTypesSerializer.globals_serializer(func)
        func_obj['__globals__'] = globs

        """write the code_object of function"""
        code = YamlTomlTypesSerializer.code_object_serializer(func.__code__)
        func_obj['__code__'] = code

        return func_obj

    @staticmethod
    def lambda_function_serializer(func: types.LambdaType) -> dict:
        res = YamlTomlTypesSerializer.user_def_function_serializer(
            func,
        )

        return res

    @staticmethod
    def builtin_function_serializer(func: types.BuiltinFunctionType) -> dict:
        """
        in module that represent BuiltinFunctionType specified only name and type
        we will find it by name in the builtins module
        """
        builtin_func_obj = {
            'type': 'BuiltinFunctionType',
            'name': func.__name__
        }

        return builtin_func_obj

    @staticmethod
    def class_instance_method_serializer(meth: types.MethodType):
        res = YamlTomlTypesSerializer.user_def_function_serializer(
            meth
        )

        return res

    @staticmethod
    def list_serializer(obj: list) -> list:

        list_obj = []
        for item in obj:

            try:

                buff = YamlTomlTypesSerializer.get_type(item)
                list_obj.append(buff)

            except TypeError as err:
                print(err)

                raise SystemExit(1)

        return list_obj

    @staticmethod
    def dict_serializer(obj: dict) -> dict:

        dict_obj = {}
        key_buff, value_buff = None, None
        for key, value in obj.items():

            """if the key is in the extra_keys then we will not serialize this item"""
            extra_keys = [
                '__module__',
                '__dict__',
                '__weakref__',
                '__doc__',
                '__hash__'
            ]
            if key not in extra_keys:

                try:

                    """determine the key type"""
                    if isinstance(key, int) or \
                            isinstance(key, float) or \
                            isinstance(key, str) or \
                            isinstance(key, bool) or \
                            isinstance(key, types.NoneType):
                        key_buff = key

                    else:

                        raise TypeError(f'keys must be str, int, float, bool or None, not {type(key)}')

                except TypeError as err:
                    print(err)

                    raise SystemExit(1)

                try:

                    """determine the value type"""
                    value_buff = YamlTomlTypesSerializer.get_type(value)

                except TypeError as err:
                    print(err)

                    raise SystemExit(1)

                finally:
                    dict_obj[key_buff] = value_buff

        return dict_obj

    @staticmethod
    def tuple_serializer(obj: tuple) -> tuple:
        res = YamlTomlTypesSerializer.list_serializer(list(obj))

        return res

    @staticmethod
    def class_serializer(obj: type) -> dict:
        """
        in key 'type' we will record 'ClassType' to determine that our object is class
        also key 'name' store the name of the class
        key 'bases' - list of the base classes
        key 'type_definition' - dict of methods and class attrs
        """
        class_obj = {}
        class_obj['type'] = 'ClassType'

        if obj.__name__ != 'object':

            buff = obj.__name__
            class_obj['name'] = buff

            buff = YamlTomlTypesSerializer.list_serializer(
                list(obj.__bases__),
            )
            class_obj['bases'] = buff

            buff = YamlTomlTypesSerializer.dict_serializer(
                obj.__dict__,
            )
            class_obj['type_definition'] = buff

        else:

            buff = obj.__name__
            class_obj['name'] = buff

        return class_obj

    @staticmethod
    def class_instance_serializer(obj: type) -> dict:
        """
        in the key 'type' wi will record 'ClassInstanceType'
        to determine that our object is class instance
        also key 'class_definition' store all information about class to create it
        key 'object_definition' - dict of methods and attrs of class instance
        """
        class_instance_obj = {}
        class_instance_obj['type'] = 'ClassInstanceType'

        buff = YamlTomlTypesSerializer.class_serializer(
            obj.__class__,
        )
        class_instance_obj['class_definition'] = buff

        buff = YamlTomlTypesSerializer.dict_serializer(
            obj.__dict__,
        )
        class_instance_obj['object_definition'] = buff

        return class_instance_obj

    @staticmethod
    def code_object_serializer(obj: types.CodeType) -> dict:
        code_obj = {}

        """this item needed to define type of the object"""
        code_obj['type'] = 'CodeType'

        """is the number of local variables used by the function"""
        co_nlocals = obj.co_nlocals
        code_obj['co_nlocals'] = co_nlocals

        """it gives the name of the function"""
        co_name = obj.co_name
        code_obj['co_name'] = co_name

        """is the total number of positional arguments"""
        co_argcount = obj.co_argcount
        code_obj['co_argcount'] = co_argcount

        """is a tuple containing the names of the local variables"""
        co_varnames = obj.co_varnames
        buff = YamlTomlTypesSerializer.tuple_serializer(co_varnames)
        code_obj['co_varnames'] = buff

        """is a tuple containing the names used by the bytecode"""
        co_names = obj.co_names
        buff = YamlTomlTypesSerializer.tuple_serializer(co_names)
        code_obj['co_names'] = buff

        """is a tuple containing the names of local variables that are
         referenced by nested functions"""
        co_cellvars = obj.co_cellvars
        buff = YamlTomlTypesSerializer.tuple_serializer(co_cellvars)
        code_obj['co_cellvars'] = buff

        """is a tuple containing the names of free variables"""
        co_freevars = obj.co_freevars
        buff = YamlTomlTypesSerializer.tuple_serializer(co_freevars)
        code_obj['co_freevars'] = buff

        """is the number of positional-only arguments"""
        co_posonlyargcount = obj.co_posonlyargcount
        code_obj['co_posonlyargcount'] = co_posonlyargcount

        """is the number of keyword-only arguments"""
        co_kwonlyargcount = obj.co_kwonlyargcount
        code_obj['co_kwonlyargcount'] = co_kwonlyargcount

        """is the first line number of the function"""
        co_firstlineno = obj.co_firstlineno
        code_obj['co_firstlineno'] = co_firstlineno

        """is a string encoding the mapping from bytecode offsets to line numbers"""
        co_lnotab = obj.co_lnotab
        buff = YamlTomlTypesSerializer.list_serializer(list(co_lnotab))
        code_obj['co_lnotab'] = buff

        """is the required stack size"""
        co_stacksize = obj.co_stacksize
        code_obj['co_stacksize'] = co_stacksize

        """is a string representing the sequence of bytecode instructions"""
        co_code = obj.co_code
        buff = YamlTomlTypesSerializer.list_serializer(list(co_code))
        code_obj['co_code'] = buff

        """is a tuple containing the literals used by the bytecode"""
        co_consts = obj.co_consts
        buff = YamlTomlTypesSerializer.tuple_serializer(co_consts)
        code_obj['co_consts'] = buff

        """is an integer encoding a number of flags for the interpreter"""
        co_flags = obj.co_flags
        code_obj['co_flags'] = co_flags

        return code_obj

    @staticmethod
    def globals_serializer(func: types.FunctionType) -> dict:
        globs_obj = {}
        globs = func.__globals__
        local_names = list(func.__code__.co_names)

        """if we have a recursion function we wrote it once"""
        if func.__name__ in local_names:
            local_names.remove(func.__name__)
            globs_obj[func.__name__] = 'recursive'

        for name in local_names:

            try:
                obj = globs[name]

            except KeyError:
                continue

            try:
                buff = YamlTomlTypesSerializer.get_type(obj)
                globs_obj[name] = buff

            except TypeError as err:
                print(err)

                raise SystemExit(1)

        return globs_obj
