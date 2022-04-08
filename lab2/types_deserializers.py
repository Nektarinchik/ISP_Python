from exceptions import JSONDecodeError


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
            if json_str[i] == start_square_bracket \
                    and not quotation_marks \
                    and len(figure_brackets) == 1 \
                    and len(square_brackets) == 0:
                square_brackets.append(start_square_bracket)
                is_list_el = True
                list_el += json_str[i]
                continue

            elif json_str[i] == start_figure_bracket \
                    and not quotation_marks \
                    and len(figure_brackets) < 2 \
                    and len(square_brackets) == 0:
                if len(figure_brackets) == 1:  # if len(figure_brackets) == 1 then it is a start of nested dictionary
                    figure_brackets.append(start_figure_bracket)
                    is_dict_el = True
                    dict_el += json_str[i]
                    continue

                else:  # if len(figure_brackets) == 0 then it is start of main dictionary
                    figure_brackets.append(start_figure_bracket)
                    continue

            elif json_str[i] == quotation_mark \
                    and len(figure_brackets) == 1 \
                    and len(square_brackets) == 0:

                if quotation_marks:  # if we have one " in quotation_marks then the string we were recording has ended
                    is_str_el = False  # then the string we were recording has ended
                    non_cont_el = ''
                    del quotation_marks[-1]
                    continue

                else:
                    quotation_marks.append(quotation_mark)  # if we have one quotation marks is empty
                    is_str_el = True  # then we start to record new string
                    continue

            elif json_str[i] == end_square_bracket \
                    and not quotation_marks \
                    and len(figure_brackets) == 1 \
                    and len(square_brackets) == 1:  # it means that our nested list has ended
                list_el += json_str[i]
                is_list_el = False
                non_cont_el = ''
                del square_brackets[-1]
                continue

            elif json_str[i] == end_figure_bracket \
                    and not quotation_marks \
                    and 1 <= len(figure_brackets) <= 2 \
                    and len(square_brackets) == 0:

                if len(figure_brackets) == 1:  # it means that our dict has ended

                    if list_el:  # record the last item

                        try:

                            value_buff = JsonTypesDeserializer.array_deserializer(list_el)

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None

                        return res

                    elif dict_el:
                        value_buff = JsonTypesDeserializer.object_deserializer(
                            dict_el
                        )
                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None

                        return res

                    elif str_el:
                        value_buff = JsonTypesDeserializer.string_deserializer(
                            str_el
                        )
                        res[key_buff] = value_buff
                        key_buff, value_buff = None, None

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

                        return res

                    else:

                        raise JSONDecodeError('incorrect JSON format')

                else:  # it is means that nested dictionary has ended
                    dict_el += json_str[i]
                    is_dict_el = False
                    non_cont_el = ''
                    del figure_brackets[-1]
                    continue

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

                        value_buff = JsonTypesDeserializer.array_deserializer(list_el)

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

            if is_list_el:
                list_el += json_str[i]

            if is_str_el:
                str_el += json_str[i]

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

            if json_str[i] == start_square_bracket \
                    and not quotation_marks \
                    and len(square_brackets) < 2 \
                    and len(figure_brackets) == 0:
                if len(square_brackets) == 1:
                    square_brackets.append(start_square_bracket)
                    is_list_el = True
                    list_el += json_str[i]
                    continue

                else:
                    square_brackets.append(start_square_bracket)
                    continue

            elif json_str[i] == start_figure_bracket \
                    and not quotation_marks \
                    and len(square_brackets) == 1 \
                    and len(figure_brackets) == 0:
                figure_brackets.append(start_figure_bracket)
                is_dict_el = True
                dict_el += json_str[i]
                continue

            elif json_str[i] == quotation_mark \
                    and len(square_brackets) == 1 \
                    and len(figure_brackets) == 0:

                if quotation_marks:
                    is_str_el = False
                    non_cont_el = ''
                    del quotation_marks[-1]
                    continue

                else:
                    quotation_marks.append(quotation_mark)
                    is_str_el = True
                    continue

            elif json_str[i] == end_figure_bracket \
                    and not quotation_marks \
                    and len(figure_brackets) == 1 \
                    and len(square_brackets) == 1:
                is_dict_el = False
                dict_el += json_str[i]
                non_cont_el = ''
                del figure_brackets[-1]
                continue

            elif json_str[i] == end_square_bracket \
                    and not quotation_marks \
                    and 1 <= len(square_brackets) <= 2 \
                    and len(figure_brackets) == 0:

                if len(square_brackets) == 1:

                    if list_el:

                        try:

                            buff = JsonTypesDeserializer.array_deserializer(list_el)

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res.append(buff)

                        return res

                    elif dict_el:
                        buff = JsonTypesDeserializer.object_deserializer(dict_el)
                        res.append(buff)

                        return res

                    elif str_el:
                        buff = JsonTypesDeserializer.string_deserializer(str_el)
                        res.append(buff)

                        return res

                    elif non_cont_el:

                        try:

                            buff = JsonTypesDeserializer.non_cont_deserializer(non_cont_el)

                        except JSONDecodeError as err:
                            print(err)

                            raise SystemExit(1)

                        res.append(buff)

                        return res

                else:
                    list_el += json_str[i]
                    is_list_el = False
                    non_cont_el = ''
                    del square_brackets[-1]
                    continue

            elif json_str[i] == comma \
                    and not quotation_marks \
                    and len(square_brackets) == 1 \
                    and len(figure_brackets) == 0:

                if list_el:

                    try:

                        buff = JsonTypesDeserializer.array_deserializer(list_el)

                    except JSONDecodeError as err:
                        print(err)

                        raise SystemExit(1)

                    res.append(buff)
                    list_el = ''
                    non_cont_el = ''
                    continue

                elif dict_el:
                    buff = JsonTypesDeserializer.object_deserializer(dict_el)
                    res.append(buff)
                    dict_el = ''
                    non_cont_el = ''
                    continue

                elif str_el:
                    buff = JsonTypesDeserializer.string_deserializer(str_el)
                    res.append(buff)
                    str_el = ''
                    non_cont_el = ''
                    continue

                elif non_cont_el:

                    try:

                        buff = JsonTypesDeserializer.non_cont_deserializer(non_cont_el)

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

            if is_list_el:
                list_el += json_str[i]

            if is_str_el:
                str_el += json_str[i]

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
