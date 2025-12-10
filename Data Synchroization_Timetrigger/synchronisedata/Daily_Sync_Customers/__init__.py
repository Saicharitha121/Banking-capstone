import logging
import azure.functions as func
import pyodbc
import os

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Daily Customer Sync started")

    # Connection string (using environment variables)
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server=tcp:sam4server.database.windows.net,1433;"
        f"Database=samdatabase;"
        f"Uid={os.getenv('SQL_USER')};"
        f"Pwd={os.getenv('SQL_PASSWORD')};"
        f"Encrypt=yes;TrustServerCertificate=no;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC usp_MergeDimCustomer")
        conn.commit()
        logging.info("Daily Customer Sync COMPLETED via MERGE")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        conn.close()