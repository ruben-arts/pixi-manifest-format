import json
import tomllib
import pytest
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError


@pytest.fixture(
    scope="module",
    params=[
        "minimal",
        "full",
        "cpp-sdl",
        "multi-machine",
        "polarify",
        "pypi",
        "solve-groups"
    ],
)
def valid_manifest(request) -> str:
    manifest_name = request.param
    with open(f"examples/valid/{manifest_name}.toml") as f:
        manifest = f.read()
    manifest_toml = tomllib.loads(manifest)
    return manifest_toml


@pytest.fixture(
    scope="module",
    params=[
        "empty",
        "no_channel",
    ],
)
def invalid_manifest(request) -> str:
    manifest_name = request.param
    with open(f"examples/invalid/{manifest_name}.toml") as f:
        manifest = f.read()
    manifest_toml = tomllib.loads(manifest)
    return manifest_toml


@pytest.fixture()
def manifest_schema():
    with open("schema.json", "r") as f:
        schema = json.load(f)
    return schema


def test_manifest_schema_valid(manifest_schema, valid_manifest):

    validate(instance=valid_manifest, schema=manifest_schema)


def test_manifest_schema_invalid(manifest_schema, invalid_manifest):
    with pytest.raises(ValidationError):
        validate(instance=invalid_manifest, schema=manifest_schema)
