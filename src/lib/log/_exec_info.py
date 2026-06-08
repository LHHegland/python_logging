"""Execution context captured at session start, used to build log headers and footers."""

import datetime
import getpass
from pathlib import Path
import platform
import sys


_ROOT_MARKERS = frozenset({'.git', '.python-version', 'pyproject.toml', 'setup.py', 'setup.cfg', 'Pipfile', 'uv.lock'})

class ExecInfo:
    """Runtime metadata for the calling module's execution session."""

    def __init__(self, entry_path: Path) -> None:
        self.entry_path: Path = entry_path
        self._set_project_path()
        self.arguments: list[str] = sys.argv[1:]
        self.user: str = getpass.getuser()
        self.system: platform.uname_result = platform.uname()
        self.python_version: str = platform.python_version()
        self.start: datetime.datetime = datetime.datetime.now(datetime.UTC)
        self.end: datetime.datetime | None = None


    def _set_project_path(self) -> None:
    
        self.project_path: Path = self.entry_path.parent

        for parent in self.entry_path.parents:
            if any((parent / m).exists() for m in _ROOT_MARKERS):
                self.project_path = parent
                break


    def elapsed(self) -> str:
        """Return a human-readable elapsed time string between start and end."""
        total = int((self.end - self.start).total_seconds() * 1_000_000)
        minutes, rem = divmod(total, 60_000_000)
        seconds, rem = divmod(rem, 1_000_000)
        ms, us = divmod(rem, 1_000)
        return f'{minutes}m {seconds}s {ms}ms {us}μs'
