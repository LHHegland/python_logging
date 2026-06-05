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
import datetime
import logging
import os
import shutil

from lib.log._exec_info import _ExecInfo
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

    def __init__(self, module_filepath: str) -> None:
        self._exec_info = _ExecInfo(module_filepath)
        logs_dir = os.path.join(self._exec_info.initial_dir, 'logs')
        created = not os.path.exists(logs_dir)
        os.makedirs(logs_dir, exist_ok=True)
        self._log = logging.getLogger()
        self._log.setLevel(logging.DEBUG)
        self._setup()
        self._log.info(self._header())
        if created:
            msg = ExceptionMessageFormatted(
                title='LOGS DIRECTORY CREATED',
                details=(
                    'Module uses logging and needs a log directory.\n'
                    f'A directory for logs did not exist in {self._exec_info.initial_dir}.\n'
                    f'Therefore, the logger created {logs_dir}.'
                ),
            )
            self.warning(str(msg))

    def __enter__(self) -> 'Log':
        return self

    def __exit__(self, *args) -> None:
        self.terminate()

    def _setup(self) -> None:
        file_handler = logging.FileHandler(
            self._exec_info.log_filepath, mode='a', encoding='utf-8'
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

    def terminate(self, dirpathname: str | None = None) -> None:
        """Write session footer, close all handlers, and optionally copy the log file.

        Args:
            dirpathname: Destination directory for a copy of the finished log.
                If None, the log remains in the logs/ directory next to the script.
        """
        self._exec_info.end = datetime.datetime.now(datetime.UTC)
        source_path = self._exec_info.log_filepath
        self._exec_info.final_dir = dirpathname
        self._log.info(self._footer())
        for handler in self._log.handlers[:]:
            handler.flush()
            handler.close()
            self._log.removeHandler(handler)
        if dirpathname is not None:
            shutil.copy(source_path, dirpathname)

    def _header(self) -> str:
        ei = self._exec_info
        return (
             'BEGIN LOGGING...\n'
            f'START: {ei.start.isoformat()}\n'
            f'USER: {ei.user}\n'
            f'OPERATING SYSTEM: {ei.system}\n'
            f'PYTHON VERSION: {ei.python_version}\n'
            f'ROOT: {os.path.join(ei.initial_dir, ei.module_basename)}.py\n'
            f'ARGUMENTS: {ei.arguments}\n'
            f'LOG: {ei.log_filepath}\n'
             '========== STARTING =========='
        )

    def _footer(self) -> str:
        ei = self._exec_info
        footer = '========== ENDING ==========\n'
        footer += 'Log copied to specified directory.\n' if ei.final_dir else '*** Final log directory not specified. ***\n'
        footer += (
            f'\nLOG: {ei.log_filepath}\n\n'
            f'  END: {ei.end.isoformat()}\n'
            f'- START: {ei.start.isoformat()}\n'
            f'= ELAPSED: {ei.elapsed()}'
        )
        return footer
