import logging

from bcra_sdk import _log


def test_logger_has_null_handler():
    assert _log.LOG_NAME == "bcra_sdk"
    assert _log.logger is logging.getLogger("bcra_sdk")
    assert any(isinstance(h, logging.NullHandler) for h in _log.logger.handlers)
