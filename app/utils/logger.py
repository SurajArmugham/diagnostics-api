import json
import logging
import sys

from datetime import datetime, timezone


# ------------------------------------------------------------
# Structured JSON Logging to stdout
#
# Why stdout (12-Factor App, factor XI):
# A containerized app never routes or stores its own log
# stream. It writes to stdout; the PLATFORM handles the rest:
#
# app stdout
#       ↓
# container runtime
#       ↓
# /var/log/containers/*.log  (on the Kubernetes node)
#       ↓
# collector DaemonSet (Alloy / Splunk forwarder / promtail)
#       ↓
# Loki / Splunk
#
# A file inside the pod is invisible to this pipeline,
# invisible to `kubectl logs`, and lost on pod restart.
#
# Why JSON:
# Each log line becomes a set of queryable FIELDS
# (level, message, custom extras) instead of prose that
# Splunk/Loki must regex-parse. Field extraction at the
# source is robust; regex at the destination is brittle.
# ------------------------------------------------------------


# ------------------------------------------------------------
# Attributes every LogRecord carries by default.
#
# Used to detect CUSTOM fields passed at the call site via:
# logger.info("msg", extra={"endpoint": "/token"})
# Anything not in this set is a custom field and gets
# promoted to a top-level JSON key.
# ------------------------------------------------------------
STANDARD_LOG_RECORD_ATTRS = set(
    logging.LogRecord(
        "", 0, "", 0, "", (), None
    ).__dict__.keys()
) | {"message", "asctime", "taskName"}


class JsonFormatter(logging.Formatter):
    """
    Render each LogRecord as one JSON object per line.

    This is what libraries like python-json-logger do
    under the hood: subclass logging.Formatter and
    override format() to return json.dumps(...).
    """

    def format(self, record: logging.LogRecord) -> str:

        log_entry = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }

        # Promote custom fields from extra={...}
        for key, value in record.__dict__.items():
            if key not in STANDARD_LOG_RECORD_ATTRS:
                log_entry[key] = value

        # Include the traceback when logging an exception
        if record.exc_info:
            log_entry["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(log_entry, default=str)


# ------------------------------------------------------------
# Configure a NAMED logger - not the root logger.
#
# basicConfig() configures the ROOT logger, which every
# library's records propagate into - their output would be
# captured into our format too. A named logger with
# propagate=False controls exactly one stream: ours.
# ------------------------------------------------------------
handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(JsonFormatter())

logger = logging.getLogger("diagnostics_api")

logger.setLevel(logging.INFO)

logger.addHandler(handler)

logger.propagate = False


# ------------------------------------------------------------
# Paramiko logs SSH transport details at INFO.
# Keep it at WARNING to avoid noise on every SSH session.
# ------------------------------------------------------------
logging.getLogger("paramiko").setLevel(
    logging.WARNING
)
