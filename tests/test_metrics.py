import re

from fastapi.testclient import TestClient

from run import app


client = TestClient(app)


def get_metric_value(metrics_text, metric_line_prefix):
    """
    Parse a metric's current value out of the Prometheus
    text format, e.g.:

    auth_failures_total{reason="bad_credentials"} 3.0

    Returns 0.0 when the series does not exist yet
    (Prometheus counters appear on first increment).
    """

    for line in metrics_text.splitlines():
        if line.startswith(metric_line_prefix):
            return float(line.rsplit(" ", 1)[1])

    return 0.0


def scrape():
    return client.get("/metrics").text


def test_metrics_endpoint_open():

    response = client.get("/metrics")

    assert response.status_code == 200

    # Prometheus text exposition format markers
    assert "# HELP" in response.text

    assert "# TYPE" in response.text


def test_request_metrics_recorded():

    client.get("/health")

    metrics = scrape()

    # Instrumentator records every request per handler
    assert re.search(
        r'http_requests_total\{.*handler="/health".*\}',
        metrics
    )


def test_auth_failure_counter():

    before = get_metric_value(
        scrape(),
        'auth_failures_total{reason="bad_credentials"}'
    )

    client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "wrongpass"
        }
    )

    after = get_metric_value(
        scrape(),
        'auth_failures_total{reason="bad_credentials"}'
    )

    assert after == before + 1


def test_invalid_token_counter():

    before = get_metric_value(
        scrape(),
        'auth_failures_total{reason="invalid_token"}'
    )

    client.get(
        "/audit-history",
        headers={
            "Authorization": "Bearer garbage"
        }
    )

    after = get_metric_value(
        scrape(),
        'auth_failures_total{reason="invalid_token"}'
    )

    assert after == before + 1


def test_token_issued_counter():

    before = get_metric_value(
        scrape(),
        "tokens_issued_total"
    )

    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )

    assert response.status_code == 200

    after = get_metric_value(
        scrape(),
        "tokens_issued_total"
    )

    assert after == before + 1
