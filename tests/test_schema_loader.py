from pathlib import Path

import pytest
from graphql import build_schema

from s2dm.exporters.utils.schema_loader import print_schema_with_directives_preserved


@pytest.fixture
def spec_directory() -> Path:
    return Path(__file__).parent.parent / "src" / "s2dm" / "spec"


def test_reference_directive_only_applied_to_supported_locations(spec_directory: Path) -> None:
    """Test that @reference is only added to types matching directive's allowed locations."""
    schema_str = """
    directive @reference(uri: String, source: String) on OBJECT | ENUM

    type TestObject { field: String }
    scalar TestScalar
    interface TestInterface { field: String }
    enum TestEnum { VALUE1 VALUE2 }
    input TestInput { field: String }
    union TestUnion = TestObject

    type Query { field: String }
    """

    schema = build_schema(schema_str)
    source_map = {
        "TestObject": "test.graphql",
        "TestScalar": "test.graphql",
        "TestInterface": "test.graphql",
        "TestEnum": "test.graphql",
        "TestInput": "test.graphql",
        "TestUnion": "test.graphql",
    }

    result = print_schema_with_directives_preserved(schema, source_map)

    assert 'type TestObject @reference(source: "test.graphql")' in result
    assert 'enum TestEnum @reference(source: "test.graphql")' in result

    assert 'scalar TestScalar @reference' not in result
    assert 'interface TestInterface @reference' not in result
    assert 'input TestInput @reference' not in result
    assert 'union TestUnion @reference' not in result


def test_reference_directive_not_applied_when_source_argument_missing() -> None:
    """Test that @reference without source argument is not applied."""
    schema_str = """
    directive @reference(uri: String!, versionTag: String) on OBJECT | ENUM

    type TestObject { field: String }
    enum TestEnum { VALUE1 VALUE2 }

    type Query { field: String }
    """

    schema = build_schema(schema_str)
    source_map = {
        "TestObject": "test.graphql",
        "TestEnum": "test.graphql",
    }

    result = print_schema_with_directives_preserved(schema, source_map)

    assert 'type TestObject @reference' not in result
    assert 'enum TestEnum @reference' not in result


def test_reference_directive_not_applied_when_directive_missing() -> None:
    """Test that compose succeeds when @reference directive is not defined."""
    schema_str = """
    type TestObject { field: String }
    enum TestEnum { VALUE1 VALUE2 }

    type Query { field: String }
    """

    schema = build_schema(schema_str)
    source_map = {
        "TestObject": "test.graphql",
        "TestEnum": "test.graphql",
    }

    result = print_schema_with_directives_preserved(schema, source_map)

    assert '@reference' not in result
    assert 'type TestObject' in result
    assert 'enum TestEnum' in result


def test_reference_directive_not_duplicated_when_already_present() -> None:
    """Test that @reference is not added if it already exists on the type."""
    schema_str = """
    directive @reference(uri: String, source: String) on OBJECT | ENUM

    type TestObject @reference(source: "original.graphql") { field: String }
    enum TestEnum { VALUE1 VALUE2 }

    type Query { field: String }
    """

    schema = build_schema(schema_str)
    source_map = {
        "TestObject": "new.graphql",
        "TestEnum": "test.graphql",
    }

    result = print_schema_with_directives_preserved(schema, source_map)

    assert 'type TestObject @reference(source: "original.graphql")' in result
    assert 'type TestObject @reference(source: "new.graphql")' not in result

    assert 'enum TestEnum @reference(source: "test.graphql")' in result


def test_reference_directive_with_all_standard_locations(spec_directory: Path) -> None:
    """Test @reference with all standard type locations from spec."""
    schema_str = """
    directive @reference(uri: String, source: String, versionTag: String) on OBJECT | INTERFACE | UNION | ENUM | ENUM_VALUE | SCALAR | INPUT_OBJECT | FIELD_DEFINITION

    type TestObject { field: String }
    interface TestInterface { field: String }
    union TestUnion = TestObject
    enum TestEnum { VALUE1 VALUE2 }
    scalar TestScalar
    input TestInput { field: String }

    type Query { field: String }
    """

    schema = build_schema(schema_str)
    source_map = {
        "TestObject": "types.graphql",
        "TestInterface": "interfaces.graphql",
        "TestUnion": "unions.graphql",
        "TestEnum": "enums.graphql",
        "TestScalar": "scalars.graphql",
        "TestInput": "inputs.graphql",
    }

    result = print_schema_with_directives_preserved(schema, source_map)

    assert 'type TestObject @reference(source: "types.graphql")' in result
    assert 'interface TestInterface @reference(source: "interfaces.graphql")' in result
    assert 'union TestUnion @reference(source: "unions.graphql")' in result
    assert 'enum TestEnum @reference(source: "enums.graphql")' in result
    assert 'scalar TestScalar @reference(source: "scalars.graphql")' in result
    assert 'input TestInput @reference(source: "inputs.graphql")' in result
