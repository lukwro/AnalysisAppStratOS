from __future__ import annotations

from dataclasses import dataclass
from typing import Any


MAX_COMPANY_NAME_LENGTH = 200


@dataclass
class CompanyRecord:
    name: str


class CompanyValidationError(ValueError):
    pass


def validate_company_name(name: Any) -> str:
    if not isinstance(name, str):
        raise CompanyValidationError("Pole 'nazwa firmy' musi byc tekstem.")

    cleaned = name.strip()
    if not cleaned:
        raise CompanyValidationError("Pole 'nazwa firmy' jest wymagane.")

    if len(cleaned) > MAX_COMPANY_NAME_LENGTH:
        raise CompanyValidationError("Nazwa firmy jest za dluga.")

    return cleaned


def create_company_record(name: Any) -> CompanyRecord:
    return CompanyRecord(name=validate_company_name(name))
