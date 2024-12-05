import pytest
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# Test: connection to the database
def test_database_connection():
    """
    Testing the connection to the database.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Execute a simple query to verify the connection
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
        # Verify that the query result is valid
        assert result == (1,), \
            "The SELECT 1 query did not return the expected value."

    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


# Test: verify that there are rows in the machines table
def test_select_machines():
    """
    Execute a simple SELECT query on the machines table
    and check that at least one row is returned.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM machines;")
                rows = cursor.fetchall()
        # Verify that at least one row was returned
        assert len(rows) > 0, \
            "The machines table is empty or does not exist."

    except Exception as e:
        pytest.fail(f"Error during query execution: {e}")


# Test: verify that there are rows in the personal_data table
def test_select_personal_data():
    """
    Execute a simple SELECT query on the personal_data table
    and check that at least one row is returned.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM personal_data;")
                rows = cursor.fetchall()
        # Verify that at least one row was returned
        assert len(rows) > 0, \
            "The personal_data table is empty or does not exist."

    except Exception as e:
        pytest.fail(f"Error during query execution: {e}")


# Test: select all the rows from maintenance_records table related to a
# specific machine
def test_select_maintenance_records():
    """
    Execute a simple SELECT query on the maintenance_records table
    and check that at least one row is returned.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM maintenance_records
                    WHERE asset_id = 'ast-yhccl1zjue2t';
                    """
                )
                rows = cursor.fetchall()
        # Verify that at least one row was returned
        assert len(rows) > 0, \
            "The maintenance_records table is empty or does not exist."

    except Exception as e:
        pytest.fail(f"Error during query execution: {e}")


# Test: select all the maintenance records related to a specific machine with
# the operator's personal data
def test_select_join_maintenance_records():
    """
    Execute a simple SELECT query on the maintenance_records table
    and check that at least one row is returned.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM maintenance_records, machines, personal_data
                    WHERE maintenance_records.asset_id = 'ast-yhccl1zjue2t'
                    AND machines.asset_id = maintenance_records.asset_id
                    AND personal_data.operator_id =
                     maintenance_records.responsible_operator_id;
                    """
                )
                rows = cursor.fetchall()
        # Verify that at least one row was returned
        assert len(rows) > 0, \
            "The maintenance_records table is empty or does not exist."

    except Exception as e:
        pytest.fail(f"Error during query execution: {e}")


# Test: insert, verify with encryption/decryption, and cleanup
def test_insert_and_decrypt_personal_data():
    """
    Test the insertion of an encrypted row, verify decryption,
    and delete the row afterward.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Define test data
                test_data = {
                    "operator_id": 11,
                    "name": "John",
                    "surname": "Doe",
                    "birth_date": "1990-01-01",
                    "document_id": "ID12345",
                    "job_role": "Engineer",
                    "iban": "IT60X0542811101000000123456",
                    "residence": "123 Test Street",
                    "contact_id": 123
                }
                secret_key = 'my_secret_key'

                # Insert an encrypted row
                cursor.execute("""
                    INSERT INTO personal_data (
                        operator_id, name, surname, birth_date, document_id,
                        job_role, iban, residence, contact_id
                    ) VALUES (
                        %(operator_id)s,
                        pgp_sym_encrypt(%(name)s, %(secret_key)s),
                        pgp_sym_encrypt(%(surname)s, %(secret_key)s),
                        %(birth_date)s,
                        pgp_sym_encrypt(%(document_id)s, %(secret_key)s),
                        pgp_sym_encrypt(%(job_role)s, %(secret_key)s),
                        pgp_sym_encrypt(%(iban)s, %(secret_key)s),
                        pgp_sym_encrypt(%(residence)s, %(secret_key)s),
                        %(contact_id)s
                    )
                """, {**test_data, "secret_key": secret_key})
                conn.commit()

                # Retrieve and decrypt the row
                cursor.execute("""
                    SELECT
                        operator_id,
                        pgp_sym_decrypt(name::bytea, %s) AS name,
                        pgp_sym_decrypt(surname::bytea, %s) AS surname,
                        birth_date,
                        pgp_sym_decrypt(document_id::bytea, %s) AS document_id,
                        pgp_sym_decrypt(job_role::bytea, %s) AS job_role,
                        pgp_sym_decrypt(iban::bytea, %s) AS iban,
                        pgp_sym_decrypt(residence::bytea, %s) AS residence,
                        contact_id
                    FROM personal_data
                    WHERE operator_id = %s
                """, (secret_key, secret_key, secret_key, secret_key, secret_key, secret_key, test_data["operator_id"]))
                decrypted_row = cursor.fetchone()

                # Verify the decrypted data matches the original
                assert decrypted_row[1] == test_data["name"], "Name decryption failed"
                assert decrypted_row[2] == test_data["surname"], "Surname decryption failed"
                assert decrypted_row[4] == test_data["document_id"], "Document ID decryption failed"
                assert decrypted_row[5] == test_data["job_role"], "Job role decryption failed"
                assert decrypted_row[6] == test_data["iban"], "IBAN decryption failed"
                assert decrypted_row[7] == test_data["residence"], "Residence decryption failed"

                # Cleanup: delete the inserted row
                cursor.execute("DELETE FROM personal_data WHERE operator_id = %s", (test_data["operator_id"],))
                conn.commit()

    except Exception as e:
        pytest.fail(f"Error during test execution: {e}")
