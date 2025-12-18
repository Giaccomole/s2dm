import tempfile
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from s2dm.exporters.utils.naming import load_naming_config
from s2dm.exporters.utils.naming_config import (
    CaseFormat,
    FieldNamingConfig,
    NamingConventionConfig,
    TypeNamingConfig,
)


class TestValidateNamingConfig:
    def test_valid_config_mixed(self) -> None:
        config: Any = {
            "type": {"object": CaseFormat.PASCAL_CASE},
            "field": {"object": CaseFormat.CAMEL_CASE, "interface": CaseFormat.CAMEL_CASE},
            "enumValue": CaseFormat.PASCAL_CASE,
            "instanceTag": CaseFormat.COBOL_CASE,
        }
        NamingConventionConfig(**config)

    def test_invalid_element_type(self) -> None:
        config: Any = {"invalid_element": "PascalCase"}
        with pytest.raises(ValidationError):
            NamingConventionConfig(**config)

    def test_invalid_case_type(self) -> None:
        config: Any = {"type": "InvalidCase"}
        with pytest.raises((ValidationError, ValueError)):
            NamingConventionConfig(**config)

    def test_invalid_context(self) -> None:
        config: Any = {"type": {"invalid_context": "PascalCase"}}
        with pytest.raises((ValidationError, ValueError)):
            NamingConventionConfig(**config)

    def test_invalid_value_type(self) -> None:
        config: Any = {"type": 123}
        with pytest.raises(ValidationError):
            NamingConventionConfig(**config)

    def test_enum_value_without_instance_tag(self) -> None:
        config: Any = {"enumValue": CaseFormat.PASCAL_CASE}
        with pytest.raises(ValueError, match="If 'enumValue' is present, 'instanceTag' must also be present"):
            NamingConventionConfig(**config)

    def test_instance_tag_without_enum_value_is_valid(self) -> None:
        config: Any = {"instanceTag": CaseFormat.COBOL_CASE}
        NamingConventionConfig(**config)

    def test_contextless_element_with_context(self) -> None:
        config: Any = {"enumValue": {"some_context": "PascalCase"}, "instanceTag": CaseFormat.PASCAL_CASE}
        with pytest.raises(ValidationError):
            NamingConventionConfig(**config)

    def test_all_valid_case_types(self) -> None:
        valid_cases = [
            CaseFormat.CAMEL_CASE,
            CaseFormat.PASCAL_CASE,
            CaseFormat.SNAKE_CASE,
            CaseFormat.KEBAB_CASE,
            CaseFormat.MACRO_CASE,
            CaseFormat.COBOL_CASE,
            CaseFormat.FLAT_CASE,
            CaseFormat.TITLE_CASE,
        ]
        for case in valid_cases:
            config: Any = {"instanceTag": case}
            NamingConventionConfig(**config)


class TestLoadNamingConfig:
    def test_load_valid_config_file(self) -> None:
        config_content = """
        type:
            object: PascalCase
            interface: PascalCase
        field:
            object: camelCase
        enumValue: PascalCase
        instanceTag: COBOL-CASE
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(config_content)
            f.flush()

            config = load_naming_config(Path(f.name))
            assert config == NamingConventionConfig(
                type=TypeNamingConfig(object=CaseFormat.PASCAL_CASE, interface=CaseFormat.PASCAL_CASE),
                field=FieldNamingConfig(object=CaseFormat.CAMEL_CASE),
                enum_value=CaseFormat.PASCAL_CASE,
                instance_tag=CaseFormat.COBOL_CASE,
            )

        Path(f.name).unlink()

    def test_load_invalid_config_file(self) -> None:
        config_content = """
        invalid_element: PascalCase
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(config_content)
            f.flush()

            with pytest.raises(ValidationError):
                load_naming_config(Path(f.name))

        Path(f.name).unlink()

    def test_load_nonexistent_file(self) -> None:
        config = load_naming_config(None)
        assert config is None

    def test_load_empty_config(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("")
            f.flush()

            config = load_naming_config(Path(f.name))
            assert config == NamingConventionConfig()

        Path(f.name).unlink()
