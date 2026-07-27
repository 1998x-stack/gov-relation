"""Unified logging configuration for the gov-relation pipeline.

Usage::

    from gov_relation.log import get_logger

    logger = get_logger(__name__)
    logger.info("Wrote GEXF: %s", path)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_LOG_CONFIGURED = False
_DEFAULT_LOG_DIR = None  # set on first init_logging call


def _default_log_dir() -> Path:
    """Lazily resolve the logs directory relative to this file's repo."""
    return Path(__file__).resolve().parents[1] / "logs"


def get_logger(name: str) -> logging.Logger:
    """Return a logger with unified formatting.

    The first call to this function performs one-time initialization
    of the root handler configuration.
    """
    global _LOG_CONFIGURED
    if not _LOG_CONFIGURED:
        _init_root()
        _LOG_CONFIGURED = True
    return logging.getLogger(name)


def _init_root() -> None:
    """Configure the root logger with a console handler (WARNING+).

    File handlers are added by ``init_logging()`` which should be called
    from the application entry point.  This minimal setup ensures log
    calls from library code always have somewhere to go.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(_formatter())
        root.addHandler(handler)


def _formatter() -> logging.Formatter:
    return logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def init_logging(log_dir: Path | None = None, level: int = logging.INFO) -> None:
    """Initialize file logging with rotation.

    Call this once from the application entry point (e.g. ``worker_loop.py``
    or ``scripts/todo_queue.py``).  Adds a rotating file handler to the
    root logger.

    Parameters
    ----------
    log_dir:
        Directory for ``gov_relation.log``.  Defaults to ``<repo>/logs/``.
    level:
        Log level for the file handler.  Default ``INFO``.
    """
    from logging.handlers import RotatingFileHandler

    global _DEFAULT_LOG_DIR
    _DEFAULT_LOG_DIR = Path(log_dir) if log_dir else _default_log_dir()
    _DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    log_path = _DEFAULT_LOG_DIR / "gov_relation.log"
    handler = RotatingFileHandler(
        str(log_path),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(_formatter())
    root.addHandler(handler)
