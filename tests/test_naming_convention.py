from graphql import build_schema

from s2dm.exporters.utils.naming_config import CaseFormat, NamingConventionConfig, ValidationMode
from s2dm.tools.naming_checker import check_naming_conventions


def test_type_name_violations() -> None:
    schema = build_schema("""
        type someType {
            field: String
        }

        type another_type {
            field: String
        }
    """)

    config = NamingConventionConfig.model_validate(
        {"type": {"object": CaseFormat.PASCAL_CASE}}, context={"mode": ValidationMode.CHECK}
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 2


def test_interface_name_violations() -> None:
    schema = build_schema("""
        interface someInterface {
            field: String
        }

        interface Another_Interface {
            field: String
        }
    """)

    config = NamingConventionConfig.model_validate(
        {"type": {"interface": CaseFormat.PASCAL_CASE}}, context={"mode": ValidationMode.CHECK}
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 2


def test_field_name_violations() -> None:
    schema = build_schema("""
        type SomeType {
            FieldName: String
            another_field: String
        }
    """)

    config = NamingConventionConfig.model_validate(
        {"field": {"object": CaseFormat.CAMEL_CASE}}, context={"mode": ValidationMode.CHECK}
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 2


def test_enum_value_violations() -> None:
    schema = build_schema("""
        enum Status {
            active
            Inactive
        }
    """)

    config = NamingConventionConfig.model_validate(
        {"enumValue": CaseFormat.MACRO_CASE}, context={"mode": ValidationMode.CHECK}
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 2


def test_argument_name_violations() -> None:
    schema = build_schema("""
        type Query {
            getUser(UserId: ID, user_name: String): String
        }
    """)

    config = NamingConventionConfig.model_validate(
        {"argument": {"field": CaseFormat.CAMEL_CASE}}, context={"mode": ValidationMode.CHECK}
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 2


def test_plural_violations() -> None:
    schema = build_schema("""
        type SomeType {
            item: [String]
            user: [String]!
        }
    """)

    config = NamingConventionConfig.model_validate({}, context={"mode": ValidationMode.CHECK})
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 2


def test_no_violations() -> None:
    schema = build_schema("""
        type SomeType {
            items: [String]
            userName: String
        }

        enum Status {
            ACTIVE
            INACTIVE
        }
    """)

    config = NamingConventionConfig.model_validate(
        {
            "type": {"object": CaseFormat.PASCAL_CASE, "enum": CaseFormat.PASCAL_CASE},
            "field": {"object": CaseFormat.CAMEL_CASE},
            "enumValue": CaseFormat.MACRO_CASE,
        },
        context={"mode": ValidationMode.CHECK},
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 0


def test_multiple_violation_types() -> None:
    schema = build_schema("""
        type some_type {
            FieldName: String
            item: [String]
            SomeInterface: some_interface
        }

        interface some_interface {
            field: String
        }

        enum status {
            Active
        }
    """)

    config = NamingConventionConfig.model_validate(
        {
            "type": {
                "object": CaseFormat.PASCAL_CASE,
                "interface": CaseFormat.PASCAL_CASE,
                "enum": CaseFormat.PASCAL_CASE,
            },
            "field": {"object": CaseFormat.CAMEL_CASE, "interface": CaseFormat.CAMEL_CASE},
            "enumValue": CaseFormat.MACRO_CASE,
        },
        context={"mode": ValidationMode.CHECK},
    )
    errors = check_naming_conventions(schema, config)

    assert len(errors) == 7
