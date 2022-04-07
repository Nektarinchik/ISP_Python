class JsonTypesDeserializer:

    @staticmethod
    def object_deserializer(json_str: str) -> dict:
        pass

    @staticmethod
    def array_deserializer(json_str: str) -> list:
        res = []
        if not json_str:
            return res

        json_str = json_str.strip()  # delete all control characters from json_str
        json_str = f',{json_str},'  # we need this for correct work of algorithm

        non_cont_obj = ''
        figure_brackets, square_brackets, quotation_marks, commas = [], [], [], []
        start_figure_bracket, start_square_bracket, quotation_mark = '{', '[', '"'
        end_figure_bracket, end_square_bracket = '}', ']'
        for i in range(len(json_str)):

            try:

                if json_str[i] == start_figure_bracket and not quotation_marks:
                    start_of_match = i
                    figure_brackets.append(start_of_match)

                elif json_str[i] == start_square_bracket and not quotation_marks:
                    start_of_match = i
                    square_brackets.append(start_of_match)

                elif json_str[i] == quotation_mark \
                        and not square_brackets \
                        and not figure_brackets:  # we check if we are in another object

                    if quotation_marks:
                        start_of_match = quotation_marks.pop()
                        buff = JsonTypesDeserializer.string_deserializer(
                            json_str[start_of_match + 1:i]
                        )

                        res.append(buff)
                        continue

                    else:
                        start_of_match = i
                        quotation_marks.append(start_of_match)

                elif json_str[i] == ',' \
                        and not figure_brackets \
                        and not square_brackets \
                        and not quotation_marks:

                    non_cont_obj = non_cont_obj.strip()

                    if '"' in non_cont_obj \
                            or '{' in non_cont_obj \
                            or '[' in non_cont_obj \
                            or not non_cont_obj:
                        non_cont_obj = ''
                        continue

                    else:

                        if non_cont_obj.isdigit() or '.' in non_cont_obj:  # then we have a number
                            buff = JsonTypesDeserializer.number_deserializer(
                                non_cont_obj
                            )
                            non_cont_obj = ''
                            res.append(buff)
                            continue

                        elif non_cont_obj in ['true', 'false']:  # then we have a bool
                            buff = JsonTypesDeserializer.bool_deserializer(
                                non_cont_obj
                            )
                            non_cont_obj = ''
                            res.append(buff)
                            continue

                        elif non_cont_obj == 'null':  # then we have a None
                            buff = None
                            non_cont_obj = ''
                            res.append(buff)
                            continue

                elif json_str[i] == end_figure_bracket and not quotation_marks:

                    if len(figure_brackets) == 1:
                        start_of_match = figure_brackets.pop()
                        buff = JsonTypesDeserializer.object_deserializer(
                            json_str[start_of_match + 1:i]
                        )

                        # вызвать функцию, что определит, что это: словарь, функция или класс
                        res.append(buff)
                        continue

                    else:
                        del figure_brackets[-1]

                elif json_str[i] == end_square_bracket and not quotation_marks:

                    if len(square_brackets) == 1:
                        start_of_match = square_brackets.pop()
                        buff = JsonTypesDeserializer.array_deserializer(
                            json_str[start_of_match + 1:i]
                        )

                        res.append(buff)
                        continue

                    else:
                        del square_brackets[-1]

                non_cont_obj += json_str[i]

            except IndexError as er:

                """index error means that the JSON format is compiled incorrectly"""
                print(er)

                return None

        return res

    @staticmethod
    def string_deserializer(json_str: str) -> str:

        return json_str

    @staticmethod
    def number_deserializer(json_str: str) -> float | int:

        res = None
        if json_str.isdigit():
            res = int(json_str)

            return res

        elif '.' in json_str:
            res = float(json_str)

            return res

        return res

    @staticmethod
    def bool_deserializer(json_str: str) -> bool:
        res = None

        if json_str == 'true':
            res = True

        elif json_str == 'false':
            res = False

        return res

    @staticmethod
    def json_string_deserializator(s: str) -> object:

        res = None
        figure_brackets, square_brackets, quotation_marks = [], [], []
        start_figure_bracket, start_square_bracket, quotation_mark = '{', '[', '"'
        end_figure_bracket, end_square_bracket = '}', ']'
        for i in range(len(s)):

            try:
                """we have to check if we are in a str"""
                if s[i] == start_figure_bracket and not quotation_marks:
                    start_of_match = i
                    figure_brackets.append(start_of_match)

                elif s[i] == start_square_bracket and not quotation_marks:
                    start_of_match = i
                    square_brackets.append(start_of_match)

                elif s[i] == quotation_mark \
                        and len(square_brackets) == 1 | 0 \
                        and len(figure_brackets) == 1 | 0:

                    if quotation_marks:
                        start_of_match = quotation_marks.pop()
                        res = JsonTypesDeserializer.string_deserializer(
                            s[start_of_match + 1:i]
                        )

                        return res

                    else:
                        start_of_match = i
                        quotation_marks.append(start_of_match)

                elif s[i] == end_figure_bracket and not quotation_marks:

                    if len(figure_brackets) == 1:
                        start_of_match = figure_brackets.pop()
                        res = JsonTypesDeserializer.object_deserializer(
                            s[start_of_match + 1:i]
                        )

                        # вызвать функцию, что определит, что это: словарь, функция или класс

                    else:
                        del figure_brackets[-1]

                elif s[i] == end_square_bracket and not quotation_marks:

                    if len(square_brackets) == 1:
                        start_of_match = square_brackets.pop()
                        res = JsonTypesDeserializer.array_deserializer(
                            s[start_of_match + 1:i]
                        )

                        return res

                    else:
                        del square_brackets[-1]

            except IndexError as er:

                """index error means that the JSON format is compiled incorrectly"""
                print(er)

                return None

        """if res is None then we have a number, bool or None"""
        if not res:

            if s.isdigit() or '.' in s:  # then we have a number
                res = JsonTypesDeserializer.number_deserializer(
                    s
                )

                return res

            elif s in ['true', 'false']:  # then we have a bool
                res = JsonTypesDeserializer.bool_deserializer(
                    s
                )

                return res

            elif s == 'null':  # then we have a None
                res = None

                return res

            else:

                return None
