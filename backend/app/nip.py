from __future__ import annotations

import re
from typing import Any


class NipValidationError(ValueError):
    pass


def validate_nip(raw_nip: Any) -> str:
    if not isinstance(raw_nip, str):
        raise NipValidationError("Parametr 'nip' musi byc tekstem.")

    cleaned = re.sub(r"\D", "", raw_nip)
    if len(cleaned) != 10:
        raise NipValidationError("NIP musi miec dokladnie 10 cyfr.")

    return cleaned
