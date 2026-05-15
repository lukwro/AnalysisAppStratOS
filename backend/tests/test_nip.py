import pytest

from backend.app.nip import NipValidationError, validate_nip


def test_validate_nip_accepts_plain_value() -> None:
    assert validate_nip("1234567890") == "1234567890"


def test_validate_nip_strips_non_digits() -> None:
    assert validate_nip("123-456-32-18") == "1234563218"


def test_validate_nip_rejects_invalid_length() -> None:
    with pytest.raises(NipValidationError):
        validate_nip("1234")
