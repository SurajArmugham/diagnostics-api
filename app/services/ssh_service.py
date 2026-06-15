import os

import paramiko

from dotenv import load_dotenv


load_dotenv()


def execute_command(command: str):
    """
    Execute a command on the target host via SSH.

    Returns:
        Command output as string.
    """

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )

    ssh.connect(
        hostname=os.getenv("SSH_HOST"),
        username=os.getenv("SSH_USER"),
        password=os.getenv("SSH_PASSWORD"),
        look_for_keys=False,
        allow_agent=False
    )

    stdin, stdout, stderr = ssh.exec_command(
        command
    )

    output = stdout.read().decode()

    ssh.close()

    return output