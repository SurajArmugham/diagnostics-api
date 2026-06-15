from app.services.ssh_service import execute_command
from app.services.db_service import save_audit_record


def get_hostname():
    """
    Retrieve hostname from target system.
    """
    return execute_command("hostname").strip()


def get_disk():
    """
    Retrieve disk usage information.
    """
    return execute_command("df -h /").strip()


def get_memory():
    """
    Retrieve memory statistics.
    """
    return execute_command("vm_stat").strip()


def get_service_status(service_name: str):
    """
    Check whether a process is running.
    """
    process_list = execute_command("ps -ef")

    if service_name.lower() in process_list.lower():
        return "RUNNING"

    return "NOT RUNNING"


def run_diagnostics(hostname: str, service_name: str):
    """
    Execute all diagnostics checks and return a consolidated response.
    """
    service_status = get_service_status(service_name)

    save_audit_record(
    hostname,
    service_name,
    service_status)

    return {
        "hostname": get_hostname(),
        "disk": get_disk(),
        "memory": get_memory(),
        "service": service_status
    }