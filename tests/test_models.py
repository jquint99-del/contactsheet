import pytest
from pydantic import ValidationError

from contactsheet.models import ExtractSpec, SheetSpec


def test_extract_spec_defaults():
    spec = ExtractSpec()
    assert spec.count == 12
    assert spec.width == 320


def test_extract_spec_rejects_zero_count():
    with pytest.raises(ValidationError):
        ExtractSpec(count=0)


def test_sheet_spec_rejects_too_many_columns():
    with pytest.raises(ValidationError):
        SheetSpec(columns=99)