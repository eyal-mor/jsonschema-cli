import yaml
import jsonschema
import argparse
import pathlib
import os
from jsonschema_cli.load import load_file, load_string
from jsonschema_cli.handlers import handle_file_uri
import enum


class ResolverChoices(enum.Enum):
    RELATIVE_PATH = 1
    ABSOLUTE_PATH = 2
    HTTP = 3


def load(data: str) -> dict:
    data_path = pathlib.Path(data).absolute()
    if os.path.isfile(data_path):
        return data_path, load_file(data_path)

    return None, load_string(data)


def create_parser():
    parser = argparse.ArgumentParser(
        "jsonschema-cli",
        description="A wrapper around https://github.com/Julian/jsonschema to validate JSON using the CLI",
    )

    parser.add_argument(
        "schema_file_or_string",
        type=str,
        help="The schema you want to use to validate the data",
    )
    parser.add_argument(
        "data_file_or_string",
        type=str,
        help="The data you want validated by the schema",
    )
    parser.add_argument(
        "-r, --resolver",
        type=str,
        help="A list of files to load for $ref to resolve too",
        choices=[""],
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    path, schema = load(args.schema_file_or_string)
    _, instance = load(args.data_file_or_string)

    if path is not None:
        handler = handle_file_uri(path)

    ref_handlers = {"": handler, "file": handler}
    resolver = jsonschema.RefResolver("", {}, handlers=ref_handlers)

    try:
        jsonschema.Draft7Validator(schema, resolver=resolver).validate(
            instance=instance
        )
    except jsonschema.ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
