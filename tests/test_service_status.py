from unittest.mock import patch

from app.services.diagnostics_service import (
    get_service_status
)


@patch(
    "app.services.diagnostics_service.execute_command"
)
def test_service_running(
    mock_execute_command
):

    mock_execute_command.return_value = """
    root 123 sshd
    root 456 python
    """

    result = get_service_status("sshd")

    assert result == "RUNNING"


@patch(
    "app.services.diagnostics_service.execute_command"
)
def test_service_not_running(
    mock_execute_command
):

    mock_execute_command.return_value = """
    root 456 python
    """

    result = get_service_status("sshd")

    assert result == "NOT RUNNING"