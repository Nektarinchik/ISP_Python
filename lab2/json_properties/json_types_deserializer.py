import builtins
import inspect
import types

from exceptions.exceptions import JSONDecodeError


class JsonTypesDeserializer:

    @staticmethod
    def object_deserializer(json_str: str) -> dict:
        res = {}

        if len(json_str) == 2:  # we have an empty dict

            return res

        key_buff, value_buff = None, None  # in these variables we will store temporary values of key and value
        is_list_el, is_dict_el, is_str_el, is_non_cont_el = False, False, False, True
        list_el, dict_el, str_el, non_cont_el = '', '', '', ''
        square_brackets, figure_brackets, quotation_marks = [], [], []
        start_figure_bracket, start_square_bracket, quotation_mark, colon = '{', '[', '"', ':'
        end_figure_bracket, end_square_bracket, comma = '}', ']', ','
        for i in range(len(json_str)):

            """check if we are not inside a string, nested dictionary or list
            before every character like {[,:]}"""
            if json_str[i] == start_square_bracket and not quotation_marks:

                if len(figure_brackets) == 1 and len(square_brackets) == 0:
                    square_brackets.append(start_square_bracket)
                    is_list_el = True
                    list_el += json_str[i]
                    continue

                else:
                    square_brackets.append(start_square_bracket)

            elif json_str[i] == start_figure_bracket and not quotation_marks:
                """if len(figure_brackets) == 1 then it is a start of nested dictionary"""
                if len(figure_brackets) == 1 and len(square_brackets) == 0:
                    figure_brackets.append(start_figure_bracket)
                    is_dict_el = True
                    dict_el += json_str[i]
                    continue

                elif len(figure_brackets) == 0 and len(square_brackets) == 0:
                    """if len(figure_brackets) == 0 then it is start of main dictionary"""
                    figure_brackets.append(start_figure_bracket)
                    continue

                else:
                    """in this case out level of nested > 2"""
                    figure_brackets.append(start_figure_bracket)

            elif json_str[i] == quotation_mark:

                if len(figure_brackets) == 1 and len(square_brackets) == 0:

                    if quotation_marks:  # if we have one " in quotation_marks then the string we were recording has ended
                        is_str_el = False  # then the string we were recording has ended
                        non_cont_el = ''
                        del quotation_marks[-1]
                        continue

                    else:
                        quotation_marks.append(quotation_mark)  # if we have one quotation marks is empty
                        is_str_el = True  # then we start to record new string
                        continue

                else:

                    if quotation_marks:
                        del quotation_marks[-1]

                    else:

                        quotation_marks.append(quotation_mark)

            elif json_str[i] == end_square_bracket and not quotation_marks:
                """it means that our nested list has ended"""
                if len(figure_brackets) == 1 and len(square_brackets) == 1:
                    list_el += json_str[i]
                    is_list_el = False
                    non_cont_el = ''
                    del square_brackets[-1]
                    continue

                else:
                    del square_brackets[-1]

            elif json_str[i] == end_figure_bracket and not quotation_marks:

                if len(figure_brackets) == 1 and len(square_brackets) == 0:  # it means that our dict has ended

                    if list_el:  # record the last item

                        try:

                            value_buff = JsonTypesDeserializer.array_deserializer(
                                list_el
                            )

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None
                        res = JsonTypesDeserializer.get_python_type_from_object(res)

                        return res

                    elif dict_el:
                        value_buff = JsonTypesDeserializer.object_deserializer(
                            dict_el
                        )
                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None
                        res = JsonTypesDeserializer.get_python_type_from_object(res)

                        return res

                    elif str_el:
                        value_buff = JsonTypesDeserializer.string_deserializer(
                            str_el
                        )
                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None
                        res = JsonTypesDeserializer.get_python_type_from_object(res)

                        return res

                    elif non_cont_el:

                        try:

                            value_buff = JsonTypesDeserializer.non_cont_deserializer(
                                non_cont_el
                            )

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None
                        res = JsonTypesDeserializer.get_python_type_from_object(res)

                        return res

                    else:

                        raise JSONDecodeError('incorrect JSON format')

                elif len(figure_brackets) == 2 and len(square_brackets) == 0:
                    """it is means that nested dictionary has ended"""
                    dict_el += json_str[i]
                    is_dict_el = False
                    non_cont_el = ''
                    del figure_brackets[-1]
                    continue

                else:
                    del figure_brackets[-1]

            elif json_str[i] == colon \
                    and not quotation_marks \
                    and len(figure_brackets) == 1 \
                    and len(square_brackets) == 0:  # in this case we record the key

                if str_el:
                    key_buff = JsonTypesDeserializer.string_deserializer(
                        str_el
                    )
                    str_el = ''
                    continue

                elif non_cont_el:

                    try:

                        key_buff = JsonTypesDeserializer.non_cont_deserializer(
                            non_cont_el
                        )

                    except JSONDecodeError as err:
                        print(err)

                        raise SystemExit(1)

                    non_cont_el = ''
                    continue

                else:

                    raise KeyError('key must be hashable')

            elif json_str[i] == comma \
                    and not quotation_marks \
                    and len(figure_brackets) == 1 \
                    and len(square_brackets) == 0:  # in this case we record value

                if list_el:

                    try:

                        value_buff = JsonTypesDeserializer.array_deserializer(
                            list_el
                        )

                    except JSONDecodeError as err:
                        print(err)

                        raise SystemExit(1)

                    res[key_buff] = value_buff
                    key_buff, value_buff = None, None
                    list_el = ''
                    non_cont_el = ''
                    continue

                elif dict_el:
                    value_buff = JsonTypesDeserializer.object_deserializer(
                        dict_el
                    )
                    res[key_buff] = value_buff
                    key_buff, value_buff = None, None
                    dict_el = ''
                    non_cont_el = ''
                    continue

                elif str_el:
                    value_buff = JsonTypesDeserializer.string_deserializer(
                        str_el
                    )
                    res[key_buff] = value_buff
                    key_buff, value_buff = None, None
                    str_el = ''
                    non_cont_el = ''
                    continue

                elif non_cont_el:

                    try:

                        value_buff = JsonTypesDeserializer.non_cont_deserializer(
                            non_cont_el
                        )

                    except JSONDecodeError as err:
                        print(err)

                        raise SystemExit(1)

                    res[key_buff] = value_buff
                    key_buff, value_buff = None, None
                    non_cont_el = ''
                    continue

                else:

                    raise JSONDecodeError('incorrect JSON format')

            if is_dict_el:
                dict_el += json_str[i]
                continue

            if is_list_el:
                list_el += json_str[i]
                continue

            if is_str_el:
                str_el += json_str[i]
                continue

            if is_non_cont_el:
                non_cont_el += json_str[i]

        return res

    @staticmethod
    def array_deserializer(json_str: str) -> list:

        res = []

        if len(json_str) == 2:  # we have an empty dict

            return res

        is_list_el, is_dict_el, is_str_el, is_non_cont_el = False, False, False, True
        list_el, dict_el, str_el, non_cont_el = '', '', '', ''
        square_brackets, figure_brackets, quotation_marks = [], [], []
        start_figure_bracket, start_square_bracket, quotation_mark = '{', '[', '"',
        end_figure_bracket, end_square_bracket, comma = '}', ']', ','
        for i in range(len(json_str)):

            if json_str[i] == start_square_bracket and not quotation_marks:
                if len(square_brackets) == 1 and len(figure_brackets) == 0:
                    square_brackets.append(start_square_bracket)
                    is_list_el = True
                    list_el += json_str[i]
                    continue

                elif len(square_brackets) == 0 and len(figure_brackets) == 0:
                    square_brackets.append(start_square_bracket)
                    continue

                else:
                    square_brackets.append(start_square_bracket)

            elif json_str[i] == start_figure_bracket and not quotation_marks:

                if len(square_brackets) == 1 and len(figure_brackets) == 0:
                    figure_brackets.append(start_figure_bracket)
                    is_dict_el = True
                    dict_el += json_str[i]
                    continue

                else:
                    figure_brackets.append(start_figure_bracket)

            elif json_str[i] == quotation_mark:

                if len(square_brackets) == 1 and len(figure_brackets) == 0:

                    if quotation_marks:
                        is_str_el = False
                        non_cont_el = ''
                        del quotation_marks[-1]
                        continue

                    else:
                        quotation_marks.append(quotation_mark)
                        is_str_el = True
                        continue

                else:

                    if quotation_marks:
                        del quotation_marks[-1]

                    else:
                        quotation_marks.append(quotation_mark)

            elif json_str[i] == end_figure_bracket and not quotation_marks:

                if len(figure_brackets) == 1 and len(square_brackets) == 1:
                    is_dict_el = False
                    dict_el += json_str[i]
                    non_cont_el = ''
                    del figure_brackets[-1]
                    continue

                else:
                    del figure_brackets[-1]

            elif json_str[i] == end_square_bracket and not quotation_marks:

                if len(square_brackets) == 1 and len(figure_brackets) == 0:

                    if list_el:

                        try:

                            buff = JsonTypesDeserializer.array_deserializer(list_el)

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res.append(buff)

                        return res

                    elif dict_el:
                        buff = JsonTypesDeserializer.object_deserializer(
                            dict_el
                        )
                        res.append(buff)

                        return res

                    elif str_el:
                        buff = JsonTypesDeserializer.string_deserializer(
                            str_el
                        )
                        res.append(buff)

                        return res

                    elif non_cont_el:

                        try:

                            buff = JsonTypesDeserializer.non_cont_deserializer(
                                non_cont_el
                            )

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res.append(buff)

                        return res

                    else:

                        raise JSONDecodeError('incorrect JSON format')

                elif len(square_brackets) == 2 and len(figure_brackets) == 0:
                    list_el += json_str[i]
                    is_list_el = False
                    non_cont_el = ''
                    del square_brackets[-1]
                    continue

                else:
                    del square_brackets[-1]

            elif json_str[i] == comma \
                    and not quotation_marks \
                    and len(square_brackets) == 1 \
                    and len(figure_brackets) == 0:

                if list_el:

                    try:

                        buff = JsonTypesDeserializer.array_deserializer(
                            list_el
                        )

                    except JSONDecodeError as err:
                        print(err)

                        raise SystemExit(1)

                    res.append(buff)
                    list_el = ''
                    non_cont_el = ''
                    continue

                elif dict_el:
                    buff = JsonTypesDeserializer.object_deserializer(
                        dict_el
                    )
                    res.append(buff)
                    dict_el = ''
                    non_cont_el = ''
                    continue

                elif str_el:
                    buff = JsonTypesDeserializer.string_deserializer(
                        str_el
                    )
                    res.append(buff)
                    str_el = ''
                    non_cont_el = ''
                    continue

                elif non_cont_el:

                    try:

                        buff = JsonTypesDeserializer.non_cont_deserializer(
                            non_cont_el
                        )

                    except JSONDecodeError as err:
                        print(err)

                        raise SystemExit(1)

                    res.append(buff)
                    non_cont_el = ''
                    continue

                else:

                    raise JSONDecodeError('incorrect JSON format')

            if is_dict_el:
                dict_el += json_str[i]
                continue

            if is_list_el:
                list_el += json_str[i]
                continue

            if is_str_el:
                str_el += json_str[i]
                continue

            if is_non_cont_el:
                non_cont_el += json_str[i]

        return res

    @staticmethod
    def string_deserializer(json_str: str) -> str:

        return json_str

    @staticmethod
    def non_cont_deserializer(json_str: str) -> float | int | bool | None:
        """this method needed to deserialize JSON objects like number, null, bool
        in Python objects like int, float, None, bool"""

        json_str = json_str.strip()
        res = None

        if json_str.isdigit():  # then we have an int
            res = int(json_str)

        elif '.' in json_str:  # then we have a float
            res = float(json_str)

        elif json_str == 'true':
            res = True

        elif json_str == 'false':
            res = False

        elif json_str == 'null':
            res = None

        else:

            raise JSONDecodeError('incorrect JSON format')

        return res

    @staticmethod
    def json_string_deserializer(s: str) -> object:
        """we call this method from json_serializer.loads and the correct JSON format
        guarantees us that we have an object, array, string, number, bool or null"""
        temp = s[0]
        start_figure_bracket, start_square_bracket, quotation_mark = '{', '[', '"'

        try:

            if temp == start_figure_bracket:  # then we have an object
                res = JsonTypesDeserializer.object_deserializer(s)

                return res

            elif temp == start_square_bracket:  # then we have an array

                try:

                    res = JsonTypesDeserializer.array_deserializer(s)

                except JSONDecodeError as err:
                    print(err)

                    raise SystemExit(1)

                return res

            elif temp == quotation_mark:  # then we have a string
                res = JsonTypesDeserializer.string_deserializer(s[1:-1])

                return res

            else:  # then we have a number, bool, null or JSON file is invalid
                res = JsonTypesDeserializer.non_cont_deserializer(s)

                return res

        except JSONDecodeError as err:
            print(err)

            raise SystemExit(1)

        except KeyError as err:
            print(err)

            raise SystemExit(1)

    @staticmethod
    def get_python_type_from_object(obj: dict):

        try:
            
            type = obj['type']
            
            if type == 'FunctionType':
                res = JsonTypesDeserializer.get_function_from_dict(obj)
                
                return res
                
            elif type == 'ClassType':
                res = JsonTypesDeserializer.get_class_from_dict(obj)

                return res

            elif type == 'BuiltinFunctionType':
                res = JsonTypesDeserializer.get_builtin_function_from_dict(obj)

                return res

            elif type == 'ClassInstanceType':
                res = JsonTypesDeserializer.get_class_instance_form_dict(obj)

                return res

            elif type == 'CodeType':
                res = JsonTypesDeserializer.get_code_object_from_dict(obj)

                return res

            else:

                return obj
            
        except KeyError:
            
            return obj
        
    @staticmethod
    def get_function_from_dict(obj: dict) -> types.FunctionType:
        is_recursive = False

        def func():
            pass

        func_globs = {}
        serialized_globs = obj['__globals__']
        for key, value in serialized_globs.items():

            if value == 'recursive':  # it means that our function is recursive
                is_recursive = True

            elif isinstance(value, dict):
                temp = JsonTypesDeserializer.get_python_type_from_object(value)

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

            elif isinstance(value, types.FunctionType):
                func_globs[key] = value

            elif isinstance(value, types.BuiltinFunctionType):
                func_globs[key] = value

            elif inspect.isclass(value):
                func_globs[key] = value

            elif inspect.isclass(type(value)):
                func_globs[key] = value

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
        co_consts = tuple(obj['co_consts'])
        co_flags = obj['co_flags']

        func_code = types.CodeType(
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
        func = types.FunctionType(func_code,
                                  func_globs,
                                  co_name
                                  )

        if is_recursive:  # if our function is recursive then we will store it in the globals
            func.__globals__[func.__name__] = func

        return func
    
    @staticmethod
    def get_builtin_function_from_dict(obj: dict) -> types.BuiltinFunctionType:
        name = obj['name']
        builtin_function_pair = dict(filter(lambda it: it[0] == name, vars(builtins).items()))
        builtin_function = builtin_function_pair[name]

        return builtin_function
    
    @staticmethod
    def get_class_from_dict(obj: dict) -> type:

        if obj['name'] == 'object':

            return object

        deserialized_bases = obj['bases']

        namespace_deserialized = {}
        namespace_serialized = obj['type_definition']
        for name, attr in namespace_serialized.items():

            if isinstance(attr, list):
                namespace_deserialized[name] = attr

            elif isinstance(attr, dict):
                temp = JsonTypesDeserializer.get_python_type_from_object(attr)

                namespace_deserialized[name] = temp

            elif isinstance(attr, str):
                namespace_deserialized[name] = attr

            elif isinstance(attr, int):
                namespace_deserialized[name] = attr

            elif isinstance(attr, float):
                namespace_deserialized[name] = attr

            elif isinstance(attr, bool):
                namespace_deserialized[name] = attr

            elif isinstance(attr, types.NoneType):
                namespace_deserialized[name] = attr

            elif isinstance(attr, types.FunctionType):
                namespace_deserialized[name] = attr

            elif isinstance(attr, types.BuiltinFunctionType):
                namespace_deserialized[name] = attr

            elif inspect.isclass(attr):
                namespace_deserialized[name] = attr

            elif inspect.isclass(type(attr)):
                namespace_deserialized[name] = attr

        name = obj['name']
        new_cl = type(name, tuple(deserialized_bases), namespace_deserialized)

        return new_cl
    
    @staticmethod
    def get_class_instance_form_dict(obj: dict) -> object:
        object_class = obj['class_definition']
        attrs = obj['object_definition']
        init_args_count = object_class.__init__.__code__.co_argcount

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
        co_consts = tuple(obj['co_consts'])
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
