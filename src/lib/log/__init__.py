"""Timestamped file logger for Python entry-point scripts.

Log acts as a session manager: it configures the root logger with file and
stderr handlers, writes a header, and tears down cleanly on exit. All modules
in the application obtain their own loggers via the standard
``logging.getLogger(__name__)`` pattern and propagate automatically.

Entry-point usage (context manager — recommended):
    import logging
    from lib.log import Log

    log = logging.getLogger(__name__)

    if __name__ == '__main__':
        with Log(__file__):
            log.info('Starting...')

Entry-point usage (manual):
    import logging
    from lib.log import Log

    log = logging.getLogger(__name__)

    if __name__ == '__main__':
        _session = Log(__file__)
        try:
            ...
        except Exception:
            log.exception('Unexpected error.')
        finally:
            _session.terminate()

Importable module usage (no setup needed — propagates to root automatically):
    import logging
    log = logging.getLogger(__name__)

Public API:
    Log: Session manager that configures the root logger for file + stderr output.
    ExceptionMessageFormatted: Structured message builder for warning/error/critical entries.
    fmt_val: Format a variable name and value for debug/info log messages.
"""
import logging
log = logging.getLogger().getChild(__name__)

import datetime
import os
from pathlib import Path
import shutil

from lib.log._exec_info import ExecInfo
from lib.log._messages import ExceptionMessageFormatted, fmt_val

__all__ = ['Log', 'ExceptionMessageFormatted', 'fmt_val']

_DATEFMT = '%Y-%m-%d %H:%M:%S %z'
_CNTXT_FLAGS = {
    'DEBUG': '⚪', 'INFO': '⬛', 'WARNING': '🟧',
    'ERROR': '🟥', 'CRITICAL': '🟥🟥',
}


class _FileFormatter(logging.Formatter):
    """Dispatches log record format and level color flag based on severity."""
    _fyi = logging.Formatter(
        '\n%(cntxt_flag)s %(message)s \n%(asctime)s - %(name)s - %(levelname)s \n',
        _DATEFMT,
    )
    _alert = logging.Formatter(
        '\n%(cntxt_flag)s %(message)s \n%(asctime)s - %(name)s - %(levelname)s \n'
        '%(threadName)s → %(processName)s \n%(pathname)s \n'
        '→ %(module)s → %(funcName)s @ %(lineno)d \nEXCEPTION INFO: %(exc_info)s \n',
        _DATEFMT,
    )

    def format(self, record: logging.LogRecord) -> str:
        """Select fyi or alert format template based on record severity, then delegate."""
        record.cntxt_flag = _CNTXT_FLAGS.get(record.levelname, '')
        return (self._fyi if record.levelno < logging.WARNING else self._alert).format(record)


class Log:
    """Session manager that configures the root logger for a script's execution.

    Creates a timestamped log file under a logs/ directory next to the calling
    script and attaches file and stderr handlers to the root logger. All
    application loggers obtained via ``logging.getLogger(__name__)`` propagate
    to these handlers automatically. Use as a context manager to ensure
    terminate() is always called:

        import logging
        from lib.log import Log

        log = logging.getLogger(__name__)

        with Log(__file__):
            log.info('Running...')
    """

    def __init__(self, entry_file: str) -> None:
        self._exec_info: ExecInfo = ExecInfo(Path(entry_file).resolve())
        self._log = logging.getLogger()
        self._log.setLevel(logging.DEBUG)

        _filename: str = f'{Path(self._exec_info.entry_path).stem}-{self._exec_info.start.strftime("%Y%m%d%H%M%S")}.log'
        self._path: Path = self._exec_info.project_path / 'logs' / _filename

        created: bool = not self._path.parent.exists()
        os.makedirs(self._path.parent, exist_ok=True)

        self._setup()

        self._log.info(self._header())

        if created:
            msg = ExceptionMessageFormatted(
                title='LOGS DIRECTORY CREATED',
                details=(
                    'Module uses logging and needs a log directory.\n'
                    f'A directory for logs did not exist in {self._exec_info.project_path}.\n'
                    f'Therefore, the logger created {self._path.parent}.'
                ),
            )
            self.warning(str(msg))


    def __enter__(self) -> 'Log':
        """Return self so the session is optionally bound via ``as``."""
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Call terminate() on block exit; exceptions are not suppressed."""
        self.terminate()

    def _setup(self) -> None:
        """Attach file and stderr handlers to the root logger."""
        file_handler = logging.FileHandler(
            self._path, mode='a', encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(_FileFormatter())
        self._log.addHandler(file_handler)

        stderr_handler = logging.StreamHandler()
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(logging.Formatter(
            '\n%(message)s \n%(asctime)s - %(name)s - %(levelname)s \n'
            '%(threadName)s → %(processName)s \n%(pathname)s \n'
            '→ %(module)s → %(funcName)s @ %(lineno)d \nEXCEPTION INFO: %(exc_info)s \n',
            _DATEFMT,
        ))
        self._log.addHandler(stderr_handler)


    def debug(self, message: str) -> None:
        """Log at DEBUG level (file only)."""
        self._log.debug(message)


    def info(self, message: str) -> None:
        """Log at INFO level (file only)."""
        self._log.info(message)


    def warning(self, message: str) -> None:
        """Log at WARNING level (file and stderr, with call-site context)."""
        self._log.warning(message)


    def error(self, message: str) -> None:
        """Log at ERROR level (file and stderr, with call-site context)."""
        self._log.error(message)


    def critical(self, message: str) -> None:
        """Log at CRITICAL level (file and stderr, with call-site context)."""
        self._log.critical(message)


    def exception(self, message: str) -> None:
        """Log at ERROR level with the current exception traceback (file and stderr)."""
        self._log.exception(message)


    def terminate(self, log_dirpath: str | None = None) -> None:
        """Write session footer, close all handlers, and optionally copy the log file.

        Args:
            log_dirpath: Destination directory path for a copy of the finished log.
                If None, the log remains in the logs/ project directory.
        """
        self._exec_info.end = datetime.datetime.now(datetime.UTC)

        self._log.info(self._footer(log_dirpath))

        for handler in self._log.handlers[:]:
            handler.flush()
            handler.close()
            self._log.removeHandler(handler)

        if log_dirpath is not None:
            shutil.copy(self._path, Path(log_dirpath).resolve())


    def _header(self) -> str:
        return (
             'BEGIN LOGGING...\n'
            f'START: {self._exec_info.start.isoformat()}\n'
            f'USER: {self._exec_info.user}\n'
            f'OPERATING SYSTEM: {self._exec_info.system}\n'
            f'PYTHON VERSION: {self._exec_info.python_version}\n'
            f'ENTRY: {self._exec_info.entry_path}\n'
            f'ARGUMENTS: {self._exec_info.arguments}\n'
            f'LOG: {self._path}\n'
             '========== STARTING =========='
        )
    

    def _footer(self, log_dirpath: str | None) -> str:
        content = '========== ENDING ==========\n'
        content += f'Log copied to {log_dirpath}.\n' if log_dirpath else '*** Final log directory not specified. Default used. ***\n'
        content += f'\nLOG: {Path(log_dirpath) / self._path.name}.\n' if log_dirpath else f'{self._path}\n'
        content += (
           f'\nEND: {self._exec_info.end.isoformat()}\n'
           f'- START: {self._exec_info.start.isoformat()}\n'
           f'= ELAPSED: {self._exec_info.elapsed()}'
        )

        return content