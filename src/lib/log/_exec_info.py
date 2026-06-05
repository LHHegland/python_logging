"""Execution context captured at session start, used to build log headers and footers."""
import datetime
import getpass
import os
import platform
import sys


class _ExecInfo:
    """Runtime metadata for the calling module's execution session."""

    def __init__(self, module_filepath: str) -> None:
        self.initial_dir: str = os.path.dirname(os.path.abspath(module_filepath))
        self.module_basename: str = os.path.splitext(os.path.basename(module_filepath))[0]
        self.arguments: list[str] = sys.argv[1:]
        self.user: str = getpass.getuser()
        self.system: platform.uname_result = platform.uname()
        self.python_version: str = platform.python_version()
        self.start: datetime.datetime = datetime.datetime.now(datetime.UTC)
        self.end: datetime.datetime | None = None
        self.final_dir: str | None = None

    @property
    def log_filepath(self) -> str:
        """Absolute path to the log file; uses final_dir once set, otherwise logs/ next to the script."""
        dirpath = self.final_dir or os.path.join(self.initial_dir, 'logs')
        name = f'{self.module_basename}_{self.start.strftime("%Y%m%d%H%M%S")}.log'
        return os.path.join(dirpath, name)

    def elapsed(self) -> str:
        """Return a human-readable elapsed time string between start and end."""
        total = int((self.end - self.start).total_seconds() * 1_000_000)
        minutes, rem = divmod(total, 60_000_000)
        seconds, rem = divmod(rem, 1_000_000)
        ms, us = divmod(rem, 1_000)
        return f'{minutes}m {seconds}s {ms}ms {us}μs'
