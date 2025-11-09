"""WGZ Core."""

from platform import system

from typing import Any


# Is current system Windows?
WINDOWS = system() == 'Windows'

# WGZ Exceptions.
class WgzMissingParameterError(Exception):
    """WGZ Missing Parameter Error."""
    def __init__(self, message: str) -> None:
        """New WGZMPE error."""
        super().__init__(message)

class WgzInvalidParameterError(Exception):
    """WGZ Invalid Parameter Error."""
    def __init__(self, message: str) -> None:
        """New WGZIPE error."""
        super().__init__(message)

class WgzStringCharacterExpectedError(Exception):
    """WGZ Character (String) Expected Error."""
    def __init__(self, message: str) -> None:
        """New WSCEE error."""
        super().__init__(message)

class WgzSingleCharacterExpectedError(Exception):
    """WGZ Single Character Character Expected Error."""
    def __init__(self, message: str) -> None:
        """New WGZSCEE error."""
        super().__init__(message)

# Ensure strings contains a single character.
def _wgz_ensure_char(expected_chr: str) -> None:
    if (c_type := type(expected_chr)) != str:
        raise WgzStringCharacterExpectedError(f'Expected a character (string), got {c_type.__name__}.')

    if (c_len := len(expected_chr)) != 1:
        raise WgzSingleCharacterExpectedError(f'Expected a single character, got {c_len} characters.')

# Adapt a constant for two platforms.
def _wgz_crossplatform_const(win: Any, posix: Any) -> Any:
    if WINDOWS:
        return win

    return posix
