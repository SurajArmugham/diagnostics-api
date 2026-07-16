import json
import logging
import sys

from app.utils.logger import JsonFormatter


def make_record(message="Test message", **extra):
    """
    Build a LogRecord the same way logging does internally,
    applying extra={...} fields like logger.info(..., extra=...)
    """

    record = logging.LogRecord(
        name="diagnostics_api",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=message,
        args=(),
        exc_info=None
    )

    for key, value in extra.items():
        setattr(record, key, value)

    return record


def test_log_output_is_valid_json():

    output = JsonFormatter().format(make_record())

    parsed = json.loads(output)

    assert parsed["level"] == "INFO"

    assert parsed["logger"] == "diagnostics_api"

    assert parsed["message"] == "Test message"

    # ISO-8601 UTC timestamp, e.g. 2026-07-16T10:32:01.123456+00:00
    assert "T" in parsed["timestamp"]

    assert parsed["timestamp"].endswith("+00:00")


def test_extra_fields_included():

    output = JsonFormatter().format(
        make_record(endpoint="/token", client_ip="10.0.0.1")
    )

    parsed = json.loads(output)

    assert parsed["endpoint"] == "/token"

    assert parsed["client_ip"] == "10.0.0.1"


def test_exception_included():

    try:
        raise ValueError("boom")
    except ValueError:
        record = make_record(message="Something failed")
        record.exc_info = sys.exc_info()

    parsed = json.loads(JsonFormatter().format(record))

    assert "exception" in parsed

    assert "ValueError: boom" in parsed["exception"]
