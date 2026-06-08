"""Formatted message helpers for log entries."""

import pprint
from dataclasses import dataclass
from typing import Any

_pp = pprint.PrettyPrinter(indent=4, width=160, compact=False, sort_dicts=False)


@dataclass
class ExceptionMessageFormatted:
    """Structured message builder for warning, error, and critical log entries.

    Attributes:
        title: Brief headline for the issue (rendered in uppercase).
        details: Explanation of what occurred and its consequences.
        suggestions: Steps the user or developer can take to resolve the issue.
    """
    title: str = ''
    details: str = ''
    suggestions: str = ''

    def __str__(self) -> str:
        """Return the formatted message string ready for use in a log call."""
        msg = f'{self.title.upper()}\n'
        if self.details:
            msg += f'DETAILS:\n{self.details}\n\n'
        if self.suggestions:
            msg += f'SUGGESTIONS:\n{self.suggestions}\n\n'
        msg += 'TRACING INFORMATION APPEARS BELOW:'
        return msg


def fmt_val(name: str, value: Any) -> str:
    """Format a variable's name, type, and value for a debug or info log message.

    Primitive types (bool, bytes, int, float, str, list, tuple, None) are
    formatted on a single line. All other types are pretty-printed across
    multiple lines.

    Args:
        name: The variable name as a string literal (e.g. ``'my_var'``).
        value: The variable's current value.

    Returns:
        A string prefixed with 🔎VarVal🔍.
    """
    if isinstance(value, (bool, bytes, int, float, str, list, tuple, type(None))):
        return f'🔎VarVal🔍 {name} ({type(value)}): {value}'
    return f'🔎VarVal🔍 {name} ({type(value)}):\n{_pp.pformat(value)}'
