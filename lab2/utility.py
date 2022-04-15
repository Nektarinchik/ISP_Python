import argparse
import os

from constants_for_utility import constants
from factory.factory import SerializerFactory
from factory.serializer_types import SerializerTypes

parser = argparse.ArgumentParser()

parser.add_argument(
    '-p',
    '--path',
    type=str,
    required=True,
    help='absolute or relative path to the file with the serialized object'
)
parser.add_argument(
    '-f',
    '--format',
    type=str,
    choices=[
        constants.JSON,
        constants.YAML,
        constants.TOML
    ],
    help='the format to be serialized to'
)

args = parser.parse_args()

# class args:
#     format = 'yaml'
#     path = r'C:\Users\MSI\Desktop\Git\ISP_Python\lab2\tests\buff.json'


if __name__ == '__main__':

    if os.path.exists(args.path):

        filename, file_extension = os.path.splitext(args.path)
        if file_extension == constants.JSON_EXT \
                and args.format == constants.JSON:
            print('the file is already in json format')

            SystemExit(0)

        if file_extension == constants.YAML_EXT \
                and args.format == constants.YAML:
            print('the file is already in yaml format')

            SystemExit(0)

        if file_extension == constants.TOML_EXT \
                and args.format == constants.TOML:
            print('the file is already in toml format')

            SystemExit(0)

        if file_extension == constants.JSON_EXT:
            json = SerializerFactory.create_serializer(SerializerTypes.json)

            with open(args.path, 'r') as f_obj:
                buff = json.load(f_obj)

            new_filename = ''
            if args.format == constants.YAML:
                new_filename = filename + constants.YAML_EXT

            elif args.format == constants.TOML:
                new_filename = filename + constants.TOML_EXT

            os.rename(args.path, new_filename)

            with open(new_filename, 'w') as f_obj:

                if args.format == constants.YAML:
                    yaml = SerializerFactory.create_serializer(SerializerTypes.yaml)
                    yaml.dump(buff, f_obj)

                elif args.format == constants.TOML:
                    toml = SerializerFactory.create_serializer(SerializerTypes.toml)
                    toml.dump(buff, f_obj)

        elif file_extension == constants.YAML_EXT:
            yaml = SerializerFactory.create_serializer(SerializerTypes.yaml)

            with open(args.path, 'r') as f_obj:
                buff = yaml.load(f_obj)

            new_filename = ''
            if args.format == constants.JSON:
                new_filename = filename + constants.JSON_EXT

            elif args.format == constants.TOML:
                new_filename = filename + constants.TOML_EXT

            os.rename(args.path, new_filename)

            with open(new_filename, 'w') as f_obj:

                if args.format == constants.JSON:
                    json = SerializerFactory.create_serializer(SerializerTypes.json)
                    json.dump(buff, f_obj)

                elif args.format == constants.TOML:
                    toml = SerializerFactory.create_serializer(SerializerTypes.toml)
                    toml.dump(buff, f_obj)

        elif file_extension == constants.TOML_EXT:
            toml = SerializerFactory.create_serializer(SerializerTypes.toml)

            with open(args.path, 'rb') as f_obj:
                buff = toml.load(f_obj)

            new_filename = ''
            if args.format == constants.JSON:
                new_filename = filename + constants.JSON_EXT

            elif args.format == constants.YAML:
                new_filename = filename + constants.YAML_EXT

            os.rename(args.path, new_filename)

            with open(new_filename, 'w') as f_obj:

                if args.format == constants.JSON:
                    json = SerializerFactory.create_serializer(SerializerTypes.json)
                    json.dump(buff, f_obj)

                elif args.format == constants.YAML:
                    yaml = SerializerFactory.create_serializer(SerializerTypes.yaml)
                    yaml.dump(buff, f_obj)

    else:
        print('File does not exist')
