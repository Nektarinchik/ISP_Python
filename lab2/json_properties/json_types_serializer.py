import code
import inspect
import types


class JsonTypesSerializer:

    @staticmethod
    def user_def_function_serializer(func: types.FunctionType, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        """start of object recording"""
        res_str += '{\n'

        """this item needed to define type of the object"""
        res_str += spaces
        res_str += '"type": "FunctionType",\n'

        """write necessary modules for working"""
        res_str += spaces
        globals = JsonTypesSerializer.globals_serializer(func, indent=indent+indent)
        res_str += f'"__globals__": {globals},\n'

        """is the number of local variables used by the function"""
        res_str += spaces
        co_nlocals = func.__code__.co_nlocals  # other items needed to serialize function
        buff = JsonTypesSerializer.int_serializer(co_nlocals)
        res_str += f'"co_nlocals": {buff},\n'

        """is the total number of positional arguments"""
        res_str += spaces
        co_argcount = func.__code__.co_argcount
        buff = JsonTypesSerializer.int_serializer(co_argcount)
        res_str += f'"co_argcount": {buff},\n'

        """is a tuple containing the names of the local variables"""
        res_str += spaces
        co_varnames = func.__code__.co_varnames
        buff = JsonTypesSerializer.tuple_serializer(co_varnames, indent=indent+indent)
        res_str += f'"co_varnames": {buff},\n'

        """is a tuple containing the names used by the bytecode"""
        res_str += spaces
        co_names = func.__code__.co_names
        buff = JsonTypesSerializer.tuple_serializer(co_names, indent=indent+indent)
        res_str += f'"co_names": {buff},\n'

        """is a tuple containing the names of local variables that are
         referenced by nested functions"""
        res_str += spaces
        co_cellvars = func.__code__.co_cellvars
        buff = JsonTypesSerializer.tuple_serializer(co_cellvars, indent=indent+indent)
        res_str += f'"co_cellvars": {buff},\n'

        """is a tuple containing the names of free variables"""
        res_str += spaces
        co_freevars = func.__code__.co_freevars
        buff = JsonTypesSerializer.tuple_serializer(co_freevars, indent=indent+indent)
        res_str += f'"co_freevars": {buff},\n'

        """is the number of positional-only arguments"""
        res_str += spaces
        co_posonlyargcount = func.__code__.co_posonlyargcount
        buff = JsonTypesSerializer.int_serializer(co_posonlyargcount)
        res_str += f'"co_posonlyargcount": {buff},\n'

        """is the number of keyword-only arguments"""
        res_str += spaces
        co_kwonlyargcount = func.__code__.co_kwonlyargcount
        buff = JsonTypesSerializer.int_serializer(co_kwonlyargcount)
        res_str += f'"co_kwonlyargcount": {buff},\n'

        """is the first line number of the function"""
        res_str += spaces
        co_firstlineno = func.__code__.co_firstlineno
        buff = JsonTypesSerializer.int_serializer(co_firstlineno)
        res_str += f'"co_firstlineno": {buff},\n'

        """is a string encoding the mapping from bytecode offsets to line numbers"""
        res_str += spaces
        co_lnotab = func.__code__.co_lnotab
        buff = JsonTypesSerializer.list_serializer(list(co_lnotab), indent=indent+indent)
        res_str += f'"co_lnotab": {buff},\n'

        """is the required stack size"""
        res_str += spaces
        co_stacksize = func.__code__.co_stacksize
        buff = JsonTypesSerializer.int_serializer(co_stacksize)
        res_str += f'"co_stacksize": {buff},\n'

        """is a string representing the sequence of bytecode instructions"""
        res_str += spaces
        co_code = func.__code__.co_code
        buff = JsonTypesSerializer.list_serializer(list(co_code), indent=indent+indent)
        res_str += f'"co_code": {buff},\n'

        """it gives the name of the function"""
        res_str += spaces
        co_name = func.__code__.co_name
        res_str += f'"co_name": "{co_name}",\n'

        """is a tuple containing the literals used by the bytecode"""
        res_str += spaces
        co_consts = func.__code__.co_consts
        buff = JsonTypesSerializer.tuple_serializer(co_consts, indent=indent+indent)
        res_str += f'"co_consts": {buff},\n'

        """is an integer encoding a number of flags for the interpreter"""
        res_str += spaces
        co_flags = func.__code__.co_flags
        buff = JsonTypesSerializer.int_serializer(co_flags)
        res_str += f'"co_flags": {buff}\n'

        """end of object recording"""
        res_str += old_spaces
        res_str += '}'

        return res_str

    """method type - the type of methods of user-defined class instances"""
    @staticmethod
    def class_instance_method_serializer(meth: types.MethodType, indent: int) -> str:
        res = JsonTypesSerializer.user_def_function_serializer(
            meth,
            indent=indent
        )

        return res

    @staticmethod
    def code_object_serializer(code_obj: types.CodeType, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        """start of object recording"""
        res_str += '{\n'

        """this item needed to define type of the object"""
        res_str += spaces
        res_str += '"type": "CodeType",\n'

        """is the number of local variables used by the function"""
        res_str += spaces
        co_nlocals = code_obj.co_nlocals  # other items needed to serialize function
        buff = JsonTypesSerializer.int_serializer(co_nlocals)
        res_str += f'"co_nlocals": {buff},\n'

        """it gives the name of the function"""
        res_str += spaces
        co_name = code_obj.co_name
        res_str += f'"co_name": "{co_name}",\n'

        """is the total number of positional arguments"""
        res_str += spaces
        co_argcount = code_obj.co_argcount
        buff = JsonTypesSerializer.int_serializer(co_argcount)
        res_str += f'"co_argcount": {buff},\n'

        """is a tuple containing the names of the local variables"""
        res_str += spaces
        co_varnames = code_obj.co_varnames
        buff = JsonTypesSerializer.tuple_serializer(co_varnames, indent=indent+indent)
        res_str += f'"co_varnames": {buff},\n'

        """is a tuple containing the names used by the bytecode"""
        res_str += spaces
        co_names = code_obj.co_names
        buff = JsonTypesSerializer.tuple_serializer(co_names, indent=indent+indent)
        res_str += f'"co_names": {buff},\n'

        """is a tuple containing the names of local variables that are
         referenced by nested functions"""
        res_str += spaces
        co_cellvars = code_obj.co_cellvars
        buff = JsonTypesSerializer.tuple_serializer(co_cellvars, indent=indent+indent)
        res_str += f'"co_cellvars": {buff},\n'

        """is a tuple containing the names of free variables"""
        res_str += spaces
        co_freevars = code_obj.co_freevars
        buff = JsonTypesSerializer.tuple_serializer(co_freevars, indent=indent+indent)
        res_str += f'"co_freevars": {buff},\n'

        """is the number of positional-only arguments"""
        res_str += spaces
        co_posonlyargcount = code_obj.co_posonlyargcount
        buff = JsonTypesSerializer.int_serializer(co_posonlyargcount)
        res_str += f'"co_posonlyargcount": {buff},\n'

        """is the number of keyword-only arguments"""
        res_str += spaces
        co_kwonlyargcount = code_obj.co_kwonlyargcount
        buff = JsonTypesSerializer.int_serializer(co_kwonlyargcount)
        res_str += f'"co_kwonlyargcount": {buff},\n'

        """is the first line number of the function"""
        res_str += spaces
        co_firstlineno = code_obj.co_firstlineno
        buff = JsonTypesSerializer.int_serializer(co_firstlineno)
        res_str += f'"co_firstlineno": {buff},\n'

        """is a string encoding the mapping from bytecode offsets to line numbers"""
        res_str += spaces
        co_lnotab = code_obj.co_lnotab
        buff = JsonTypesSerializer.list_serializer(list(co_lnotab), indent=indent+indent)
        res_str += f'"co_lnotab": {buff},\n'

        """is the required stack size"""
        res_str += spaces
        co_stacksize = code_obj.co_stacksize
        buff = JsonTypesSerializer.int_serializer(co_stacksize)
        res_str += f'"co_stacksize": {buff},\n'

        """is a string representing the sequence of bytecode instructions"""
        res_str += spaces
        co_code = code_obj.co_code
        buff = JsonTypesSerializer.list_serializer(list(co_code), indent=indent+indent)
        res_str += f'"co_code": {buff},\n'

        """is a tuple containing the literals used by the bytecode"""
        res_str += spaces
        co_consts = code_obj.co_consts
        buff = JsonTypesSerializer.tuple_serializer(co_consts, indent=indent+indent)
        res_str += f'"co_consts": {buff},\n'

        """is an integer encoding a number of flags for the interpreter"""
        res_str += spaces
        co_flags = code_obj.co_flags
        buff = JsonTypesSerializer.int_serializer(co_flags)
        res_str += f'"co_flags": {buff}\n'

        """end of object recording"""
        res_str += old_spaces
        res_str += '}'

        return res_str

    @staticmethod
    def lambda_function_serializer(func: types.LambdaType, indent: int) -> str:
        res = JsonTypesSerializer.user_def_function_serializer(
            func,
            indent=indent
        )

        return res

    @staticmethod
    def builtin_function_serializer(func: types.BuiltinFunctionType, indent: int) -> str:
        """in module that represent BuiltinFunctionType specified only name and type
        we will find it by name in the builtins module"""
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        res_str += '{\n'

        res_str += spaces
        res_str += '"type": "BuiltinFunctionType",\n'

        res_str += spaces
        res_str += f'"name": "{func.__name__}"\n'

        res_str += old_spaces
        res_str += '}'

        return res_str

    @staticmethod
    def globals_serializer(func: types.FunctionType, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''
        globals = func.__globals__
        local_names = list(func.__code__.co_names)

        """if globals is empty write down the {}"""
        if globals:
            res_str += '{\n'

        else:
            res_str += '{'
            old_spaces = ''

        """if we have a recursion function we write it once"""
        if func.__name__ in local_names:
            local_names.remove(func.__name__)
            res_str += spaces
            res_str += f'"{func.__name__}": "recursive",\n'

        value_buff = None
        counter = 0
        for name in local_names:
            counter += 1

            try:
                obj = globals[name]

            except KeyError as err:
                continue

            try:
                """the beginning of a series of conditional operators to 
                determine the global object type"""
                if isinstance(obj, int):
                    value_buff = JsonTypesSerializer.int_serializer(
                        obj
                    )

                elif isinstance(obj, types.FunctionType):
                    value_buff = JsonTypesSerializer.user_def_function_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif isinstance(obj, types.MethodType):
                    value_buff = JsonTypesSerializer.class_instance_method_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif isinstance(obj, types.LambdaType):
                    value_buff = JsonTypesSerializer.lambda_function_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif isinstance(obj, types.BuiltinFunctionType):
                    value_buff = JsonTypesSerializer.builtin_function_serializer(
                        obj, indent=indent + indent
                    )

                elif isinstance(obj, float):
                    value_buff = JsonTypesSerializer.float_serializer(
                        obj
                    )

                elif isinstance(obj, str):
                    value_buff = f'"{obj}"'

                elif isinstance(obj, list):
                    value_buff = JsonTypesSerializer.list_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif isinstance(obj, dict):
                    value_buff = JsonTypesSerializer.dict_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif isinstance(obj, tuple):
                    value_buff = JsonTypesSerializer.tuple_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif isinstance(obj, bool):
                    value_buff = JsonTypesSerializer.bool_serializer(
                        obj
                    )

                elif isinstance(obj, types.NoneType):
                    value_buff = JsonTypesSerializer.none_serializer()

                elif inspect.isclass(obj):
                    value_buff = JsonTypesSerializer.class_serializer(
                        obj,
                        indent=indent + indent
                    )

                elif inspect.iscode(obj):
                    value_buff = JsonTypesSerializer.code_object_serializer(
                        obj,
                        indent=indent+indent
                    )

                elif isinstance(obj, types.ModuleType):
                    continue

                elif inspect.isclass(type(obj)):
                    value_buff = JsonTypesSerializer.class_instance_serializer(
                        obj,
                        indent=indent + indent
                    )

                else:

                    raise TypeError(f'Object of {type(obj)} is not JSON serializable')

            except TypeError as err:
                print(err)

                raise SystemExit(1)

            if counter == len(local_names):
                res_str += spaces
                res_str += f'"{name}": {value_buff}\n'
            else:
                res_str += spaces
                res_str += f'"{name}": {value_buff},\n'

        """we need this conditional operator to close the dict"""
        if len(res_str) > 2:

            if res_str[-2] != ',':
                res_str = res_str[:-1]
                res_str += ',\n'

        """save the names of the modules connected in this module so that we can load them later"""
        value = 'module'
        for key in globals.keys():

            if isinstance(globals[key], types.ModuleType):
                name = globals[key].__name__
                res_str += spaces
                res_str += f'"{name}": "{value}",\n'

            else:
                continue

        """we need this conditional operator to close the dict"""
        if res_str[-2] == ',':
            res_str = res_str[:-2]
            res_str += '\n'

        if res_str == '{\n':
            res_str = '{}'

        else:
            res_str += old_spaces
            res_str += '}'

        return res_str

    @staticmethod
    def class_serializer(obj: type, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        if obj:
            res_str += '{\n'

        else:
            res_str += '{'
            old_spaces = ''

        res_str += spaces
        res_str += f'"type": "ClassType",\n'

        if obj.__name__ != 'object':

            res_str += spaces
            buff = obj.__name__
            res_str += f'"name": "{buff}",\n'

            res_str += spaces
            buff = JsonTypesSerializer.list_serializer(
                list(obj.__bases__),
                indent=indent+indent
            )
            res_str += f'"bases": {buff},\n'

            res_str += spaces

            buff = JsonTypesSerializer.dict_serializer(
                obj.__dict__,
                indent=indent+indent
            )
            res_str += f'"type_definition": {buff}\n'

        else:

            res_str += spaces
            buff = obj.__name__
            res_str += f'"name": "{buff}"\n'

        res_str += old_spaces
        res_str += '}'

        return res_str

    @staticmethod
    def class_instance_serializer(obj: type, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        if obj:
            res_str += '{\n'

        else:
            res_str += '{'
            old_spaces = ''

        res_str += spaces
        res_str += f'"type": "ClassInstanceType",\n'

        res_str += spaces
        buff = obj.__class__.__name__
        res_str += f'"class_name": "{buff}",\n'

        res_str += spaces
        buff = JsonTypesSerializer.class_serializer(
            obj.__class__,
            indent=indent+indent
        )
        res_str += f'"class_definition": {buff},\n'

        res_str += spaces
        buff = JsonTypesSerializer.dict_serializer(
            obj.__dict__,
            indent=indent+indent
        )
        res_str += f'"object_definition": {buff}\n'

        res_str += old_spaces
        res_str += '}'

        return res_str

    @staticmethod
    def int_serializer(obj: int) -> str:

        if isinstance(obj, bool):
            res = JsonTypesSerializer.bool_serializer(
                obj
            )

        else:
            res = str(obj)

        return res

    @staticmethod
    def list_serializer(obj: list, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        if obj:
            res_str += '[\n'

        else:
            res_str += '['
            old_spaces = ''

        counter = 0
        for item in obj:
            counter += 1

            try:

                if isinstance(item, types.FunctionType):
                    buff = JsonTypesSerializer.user_def_function_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, types.MethodType):
                    buff = JsonTypesSerializer.class_instance_method_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, types.LambdaType):
                    buff = JsonTypesSerializer.lambda_function_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, types.BuiltinFunctionType):
                    buff = JsonTypesSerializer.builtin_function_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, int):
                    temp = JsonTypesSerializer.int_serializer(
                        item
                    )
                    buff = temp

                elif isinstance(item, float):
                    temp = JsonTypesSerializer.float_serializer(
                        item
                    )
                    buff = temp

                elif isinstance(item, str):
                    buff = f'"{item}"'

                elif isinstance(item, list):
                    buff = JsonTypesSerializer.list_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, dict):
                    buff = JsonTypesSerializer.dict_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, tuple):
                    buff = JsonTypesSerializer.tuple_serializer(
                        item,
                        indent=indent+indent
                    )

                elif isinstance(item, bool):
                    temp = JsonTypesSerializer.bool_serializer(
                        item
                    )
                    buff = temp

                elif isinstance(item, types.NoneType):
                    temp = JsonTypesSerializer.none_serializer()
                    buff = temp

                elif inspect.isclass(item):
                    buff = JsonTypesSerializer.class_serializer(
                        item,
                        indent=indent+indent
                    )

                elif inspect.iscode(item):
                    buff = JsonTypesSerializer.code_object_serializer(
                        item,
                        indent=indent+indent
                    )

                elif inspect.isclass(type(item)):
                    buff = JsonTypesSerializer.class_instance_serializer(
                        item,
                        indent=indent+indent
                    )

                else:

                    raise TypeError(f'Object of {type(item)} is not JSON serializable')

            except TypeError as err:
                print(err)

                raise SystemExit(1)

            finally:

                if counter != len(obj):
                    res_str += spaces
                    res_str += f'{buff},\n'

                else:
                    res_str += spaces
                    res_str += f'{buff}\n'

        res_str += old_spaces
        res_str += ']'

        return res_str

    @staticmethod
    def dict_serializer(obj: dict, indent: int) -> str:
        old_spaces = ''

        if int(indent / 2) != 1:
            old_spaces = int(indent / 2) * ' '

        spaces = indent * ' '
        res_str = ''

        """if obj is empty write down the {}"""
        if obj:
            res_str += '{\n'

        else:
            res_str += '{'
            old_spaces = ''

        key_buff, value_buff = '', ''
        counter = 0  # this counter need to find the last element
        for key, value in obj.items():
            counter += 1
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

                    """the beginning of a series of conditional operators to 
                    determine the key type"""
                    if isinstance(key, int):
                        temp = JsonTypesSerializer.int_serializer(
                            key
                        )
                        key_buff = f'"{temp}"'

                    elif isinstance(key, float):
                        temp = JsonTypesSerializer.float_serializer(
                            key
                        )
                        key_buff = f'"{temp}"'

                    elif isinstance(key, str):
                        key_buff = f'"{key}"'

                    elif isinstance(key, bool):
                        temp = JsonTypesSerializer.bool_serializer(
                            key
                        )
                        key_buff = f'"{temp}"'

                    elif isinstance(key, types.NoneType):
                        temp = JsonTypesSerializer.none_serializer()
                        key_buff = f'"{temp}"'

                    else:

                        raise TypeError(f'keys must be str, int, float, bool or None, not {type(key)}')

                except TypeError as err:
                    print(err)

                    raise SystemExit(1)
                    """end of a series of conditional operators to 
                    determine the key type"""

                try:

                    """the beginning of a series of conditional operators to 
                    determine the value type"""
                    if isinstance(value, int):
                        temp = JsonTypesSerializer.int_serializer(
                            value
                        )
                        value_buff = temp

                    elif isinstance(value, types.FunctionType):
                        value_buff = JsonTypesSerializer.user_def_function_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif isinstance(value, types.MethodType):
                        value_buff = JsonTypesSerializer.class_instance_method_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif isinstance(value, types.LambdaType):
                        value_buff = JsonTypesSerializer.lambda_function_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif isinstance(value, types.BuiltinFunctionType):
                        value_buff = JsonTypesSerializer.builtin_function_serializer(
                            value, indent=indent+indent
                        )

                    elif isinstance(value, float):
                        temp = JsonTypesSerializer.float_serializer(
                            value
                        )
                        value_buff = temp

                    elif isinstance(value, str):
                        value_buff = f'"{value}"'

                    elif isinstance(value, list):
                        value_buff = JsonTypesSerializer.list_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif isinstance(value, dict):
                        value_buff = JsonTypesSerializer.dict_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif isinstance(value, tuple):
                        value_buff = JsonTypesSerializer.tuple_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif isinstance(value, bool):
                        temp = JsonTypesSerializer.bool_serializer(
                            value
                        )
                        value_buff = temp

                    elif isinstance(value, types.NoneType):
                        temp = JsonTypesSerializer.none_serializer()
                        value_buff = temp

                    elif inspect.isclass(value):
                        value_buff = JsonTypesSerializer.class_serializer(
                            value,
                            indent=indent+indent
                        )

                    elif inspect.iscode(value):
                        value_buff = JsonTypesSerializer.code_object_serializer(
                            value,
                            indent=indent
                        )

                    elif inspect.isclass(type(value)):
                        value_buff = JsonTypesSerializer.class_instance_serializer(
                            value,
                            indent=indent+indent
                        )

                    else:

                        raise TypeError(f'Object of {type(value)} is not JSON serializable')

                except TypeError as err:
                    print(err)

                    raise SystemExit(1)

                finally:

                    if counter == len(obj):
                        res_str += spaces
                        res_str += f'{key_buff}: {value_buff}\n'

                    else:
                        res_str += spaces
                        res_str += f'{key_buff}: {value_buff},\n'

        """we need this conditional operator to close the dict"""
        if len(res_str) > 2:

            if res_str[-2] == ',':
                res_str = res_str[:-2]
                res_str += '\n'

        if res_str == '{\n':
            res_str = '{}'

        else:

            if res_str == '{':
                res_str += '}'

            else:

                res_str += old_spaces
                res_str += '}'

        return res_str

    @staticmethod
    def tuple_serializer(obj: tuple, indent: int) -> str:
        res = JsonTypesSerializer.list_serializer(list(obj), indent=indent)

        return res

    @staticmethod
    def bool_serializer(obj: bool) -> str:
        res = str(obj).lower()

        return res

    @staticmethod
    def float_serializer(obj: float):
        res = str(obj)

        return res

    @staticmethod
    def none_serializer() -> str:
        res = 'null'

        return res