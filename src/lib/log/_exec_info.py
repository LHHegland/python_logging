"""Execution context captured at session start, used to build log headers and footers."""
import logging
log = logging.getLogger().getChild(__name__)

import datetime
import getpass
from pathlib import Path
import platform
import sys


class ExecInfo:
    """Runtime metadata for the calling module's execution session."""

    def __init__(self, entry_path: Path) -> None:
        self.entry_path: Path = entry_path
        self.project_path: Path = self.entry_path.parent.parent if self.entry_path.parent.name == 'src' else self.entry_path.parent
        self.arguments: list[str] = sys.argv[1:]
        self.user: str = getpass.getuser()
        self.system: platform.uname_result = platform.uname()
        self.python_version: str = platform.python_version()
        self.start: datetime.datetime = datetime.datetime.now(datetime.UTC)
        self.end: datetime.datetime | None = None


    def elapsed(self) -> str:
        """Return a human-readable elapsed time string between start and end."""
        total = int((self.end - self.start).total_seconds() * 1_000_000)
        minutes, rem = divmod(total, 60_000_000)
        seconds, rem = divmod(rem, 1_000_000)
        ms, us = divmod(rem, 1_000)
        return f'{minutes}m {seconds}s {ms}ms {us}μs'
