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

        """is the number of local variables used by the function"""
        res_str += spaces
        co_nlocals = func.__code__.co_nlocals  # other items needed to serialize function
        buff = JsonTypesSerializer.int_serializer(co_nlocals)
        res_str += f'"co_nlocals": "{buff}",\n'

        """is the total number of positional arguments"""
        res_str += spaces
        co_argcount = func.__code__.co_argcount
        buff = JsonTypesSerializer.int_serializer(co_argcount)
        res_str += f'"co_argcount": "{buff}",\n'

        """is a tuple containing the names of the local variables"""
        res_str += spaces
        co_varnames = func.__code__.co_varnames
        buff = JsonTypesSerializer.tuple_serializer(co_varnames, indent=indent + indent)
        res_str += f'"co_varnames": {buff},\n'

        """is a tuple containing the names used by the bytecode"""
        res_str += spaces
        co_names = func.__code__.co_names
        buff = JsonTypesSerializer.tuple_serializer(co_names, indent=indent + indent)
        res_str += f'"co_names": {buff},\n'

        """is a tuple containing the names of local variables that are
         referenced by nested functions"""
        res_str += spaces
        co_cellvars = func.__code__.co_cellvars
        buff = JsonTypesSerializer.tuple_serializer(co_cellvars, indent=indent + indent)
        res_str += f'"co_cellvars": {buff},\n'

        """is a tuple containing the names of free variables"""
        res_str += spaces
        co_freevars = func.__code__.co_freevars
        buff = JsonTypesSerializer.tuple_serializer(co_freevars, indent=indent + indent)
        res_str += f'"co_freevars": {buff},\n'

        """is the number of positional-only arguments"""
        res_str += spaces
        co_posonlyargcount = func.__code__.co_posonlyargcount
        buff = JsonTypesSerializer.int_serializer(co_posonlyargcount)
        res_str += f'"co_posonlyargcount": "{buff}",\n'

        """is the number of keyword-only arguments"""
        res_str += spaces
        co_kwonlyargcount = func.__code__.co_kwonlyargcount
        buff = JsonTypesSerializer.int_serializer(co_kwonlyargcount)
        res_str += f'"co_kwonlyargcount": "{buff}",\n'

        """is the first line number of the function"""
        res_str += spaces
        co_firstlineno = func.__code__.co_firstlineno
        buff = JsonTypesSerializer.int_serializer(co_firstlineno)
        res_str += f'"co_firstlineno": {buff},\n'

        """is a string encoding the mapping from bytecode offsets to line numbers"""
        res_str += spaces
        co_lnotab = func.__code__.co_lnotab
        res_str += f'"co_lnotab": "{co_lnotab}",\n'

        """is the required stack size"""
        res_str += spaces
        co_stacksize = func.__code__.co_stacksize
        buff = JsonTypesSerializer.int_serializer(co_stacksize)
        res_str += f'"co_stacksize": "{buff}",\n'

        """is a string representing the sequence of bytecode instructions"""
        res_str += spaces
        co_code = func.__code__.co_code
        res_str += f'"co_code": "{co_code}",\n'

        """is a tuple containing the literals used by the bytecode"""
        res_str += spaces
        co_consts = func.__code__.co_consts
        buff = JsonTypesSerializer.tuple_serializer(co_consts, indent=indent + indent)
        res_str += f'"co_consts": {buff},\n'

        """is an integer encoding a number of flags for the interpreter"""
        res_str += spaces
        co_flags = func.__code__.co_flags
        buff = JsonTypesSerializer.int_serializer(co_flags)
        res_str += f'"co_flags": "{buff}"\n'

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
    def class_serializer(obj: type, indent: int) -> str:
        pass

    @staticmethod
    def class_instance_serializer(obj: type, indent: int) -> str:
        pass

    @staticmethod
    def int_serializer(obj: int) -> str:
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

        for item in obj:

            try:

                if isinstance(item, types.FunctionType):
                    buff = JsonTypesSerializer.user_def_function_serializer(
                        item,
                        indent=indent + indent
                    )

                elif isinstance(item, types.LambdaType):
                    buff = JsonTypesSerializer.lambda_function_serializer(
                        item,
                        indent=indent + indent
                    )

                elif isinstance(item, int):
                    temp = JsonTypesSerializer.int_serializer(
                        item
                    )
                    buff = f'"{temp}"'

                elif isinstance(item, float):
                    temp = JsonTypesSerializer.float_serializer(
                        item
                    )
                    buff = f'"{temp}"'

                elif isinstance(item, str):
                    buff = f'"{item}"'

                elif isinstance(item, list):
                    buff = JsonTypesSerializer.list_serializer(
                        item,
                        indent=indent + indent
                    )

                elif isinstance(item, dict):
                    buff = JsonTypesSerializer.dict_serializer(
                        item,
                        indent=indent + indent
                    )

                elif isinstance(item, tuple):
                    buff = JsonTypesSerializer.tuple_serializer(
                        item,
                        indent=indent + indent
                    )

                elif isinstance(item, bool):
                    temp = JsonTypesSerializer.bool_serializer(
                        item
                    )
                    buff = f'"{temp}"'

                elif isinstance(item, types.NoneType):
                    temp = JsonTypesSerializer.none_serializer()
                    buff = f'"{temp}"'

                elif inspect.isclass(item):
                    buff = JsonTypesSerializer.class_serializer(
                        item,
                        indent=indent + indent
                    )

                elif inspect.isclass(type(item)):
                    buff = JsonTypesSerializer.class_instance_serializer(
                        item,
                        indent=indent + indent
                    )

                else:

                    raise TypeError(f'Object of {type(item)} is not JSON serializable')

            except TypeError as err:
                print(err)
                temp = JsonTypesSerializer.none_serializer()
                buff = f'"{temp}"'

            finally:

                if item is not obj[-1]:
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
        pass

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
