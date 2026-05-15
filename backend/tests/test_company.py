import pytest

from backend.app.company import (
    CompanyValidationError,
    MAX_COMPANY_NAME_LENGTH,
    create_company_record,
    validate_company_name,
)


def test_validate_company_name_accepts_trimmed_value() -> None:
    assert validate_company_name("  ACME SA  ") == "ACME SA"


def test_validate_company_name_rejects_empty() -> None:
    with pytest.raises(CompanyValidationError):
        validate_company_name("   ")


def test_validate_company_name_rejects_too_long() -> None:
    too_long = "A" * (MAX_COMPANY_NAME_LENGTH + 1)
    with pytest.raises(CompanyValidationError):
        validate_company_name(too_long)


def test_create_company_record_returns_valid_record() -> None:
    record = create_company_record("Firma Testowa")
    assert record.name == "Firma Testowa"
