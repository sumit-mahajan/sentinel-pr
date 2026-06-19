from pydantic import BaseModel

from infrastructure.ai.gemini_client import _gemini_schema


class _Finding(BaseModel):
    title: str
    severity: str | None = None


class _Output(BaseModel):
    findings: list[_Finding]


def test_gemini_schema_inlines_defs_and_strips_metadata() -> None:
    schema = _gemini_schema(_Output)

    assert "$defs" not in schema
    assert "$schema" not in schema
    assert "findings" in schema["properties"]
    assert schema["properties"]["findings"]["type"] == "array"


def test_gemini_schema_preserves_title_field_name_in_properties() -> None:
    schema = _gemini_schema(_Finding)

    assert "title" in schema["properties"]
