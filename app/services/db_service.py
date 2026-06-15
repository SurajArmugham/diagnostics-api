import os
import time

import psycopg2

from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    """
    Create database connection with retry logic.
    """

    for _ in range(10):

        try:

            return psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )

        except psycopg2.OperationalError:

            time.sleep(2)

    raise Exception("Unable to connect to database.")


def save_audit_record(
    hostname: str,
    service: str,
    service_status: str
):
    """
    Insert diagnostics audit record.
    """
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO diagnostics_audit
        (
            hostname,
            service,
            service_status
        )
        VALUES
        (%s, %s, %s)
        """,
        (
            hostname,
            service,
            service_status
        )
    )

    connection.commit()

    cursor.close()

    connection.close()


def get_audit_history():
    """
    Retrieve diagnostics audit history.
    """
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            hostname,
            service,
            service_status,
            created_at
        FROM diagnostics_audit
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    cursor.close()

    connection.close()

    return rows

 
def create_audit_table():
    """
    Create audit table if it does not exist.
    """
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS diagnostics_audit (

            id SERIAL PRIMARY KEY,

            hostname VARCHAR(255),

            service VARCHAR(255),

            service_status VARCHAR(50),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    cursor.close()

    connection.close()