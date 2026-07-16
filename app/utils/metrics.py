from prometheus_client import Counter


# ------------------------------------------------------------
# Custom Application Metrics
#
# Counter:
# A value that only ever INCREASES (resets to 0 on pod
# restart). Prometheus turns counters into rates with
# PromQL, e.g.:
#
#   rate(auth_failures_total[5m])
#
# "auth failures per second over the last 5 minutes" -
# the basis of a Grafana panel or an alert rule.
#
# Label Cardinality (interview essential):
# Every distinct label value creates a NEW time series.
# Labels must be a small BOUNDED set:
#
#   reason="bad_credentials" | "invalid_token"     GOOD (2)
#   username="..."  / client_ip="..."              BAD (unbounded,
#                                                   series explosion)
#
# Per-replica note:
# Each pod counts its OWN traffic. Prometheus scrapes
# every pod individually; totals come from PromQL:
#
#   sum(rate(auth_failures_total[5m]))
# ------------------------------------------------------------

TOKENS_ISSUED = Counter(
    "tokens_issued_total",
    "JWTs issued after successful login"
)

AUTH_FAILURES = Counter(
    "auth_failures_total",
    "Authentication failures by reason",
    ["reason"]
)
