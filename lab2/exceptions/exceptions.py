class JSONDecodeError(Exception):

    def __init__(self, message):
        self.__message = message

    def __str__(self):

        return self.__message


class YAMLDecodeError(Exception):

    def __init__(self, message):
        self.__message = message

    def __str__(self):

        return self.__message
