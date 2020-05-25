# JsonSchema CLI

A thin wrapper over [Python Jsonschema](https://github.com/Julian/jsonschema) to allow validating shcemas easily using simple CLI commands.

## Installing

`pip install jsonschema-cli`

## Usgae

Using `jsonschema-cli --help`

```bash
usage: jsonschema-cli [-h] [-r, --resolver {}] schema_file_or_string data_file_or_string

A wrapper around https://github.com/Julian/jsonschema to validate JSON using the CLI

positional arguments:
  schema_file_or_string
                        The schema you want to use to validate the data
  data_file_or_string   The data you want validated by the schema

optional arguments:
  -h, --help            show this help message and exit
  -r, --resolver {}     A list of files to load for $ref to resolve too
```

### Examples

```bash
# Returns no errors on stdout, no output needed on success (just exit code 0 is enough)
jsonschema-cli validate '{"properties": {"number": {"type": "integer"}}, "required": ["number"]}' '{"number": 123}'
# Has an error, "number" is now "123" instead of 123, an integer is expected.
jsonschema-cli validate '{"properties": {"number": {"type": "integer"}}, "required": ["number"]}' '{"number": "123"}'
> '123' is not of type 'integer'
>
> Failed validating 'type' in schema['properties']['number']:
>     {'type': 'integer'}
>
> On instance['number']:
>     '123'
```

## Load YAML

The CLI command can read YAML and validate both schema and data written in YAML

```bash
# Returns no errors on stdout, no output needed on success (just exit code 0 is enough)
SCHEMA="
properties:
  number:
    type: integer
"
DATA="
number: 123
"
jsonschema-cli validate "$SCHEMA" "$DATA"
# Has an error, "number" is now "123" instead of 123, an integer is expected.
SCHEMA="
properties:
  number:
    type: integer
"
DATA="
number: \"123\"
"
jsonschema-cli validate "$SCHEMA" "$DATA"
> '123' is not of type 'integer'
>
> Failed validating 'type' in schema['properties']['number']:
>     {'type': 'integer'}
>
> On instance['number']:
>     '123'
```