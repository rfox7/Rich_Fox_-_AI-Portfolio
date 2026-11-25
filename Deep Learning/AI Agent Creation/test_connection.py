import os, time
import pyodbc
from dotenv import load_dotenv

load_dotenv()

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{os.getenv('AZURE_SQL_SERVER')},1433;"
    f"Database={os.getenv('AZURE_SQL_DATABASE')};"
    f"Uid={os.getenv('AZURE_SQL_USER')};"
    f"Pwd={os.getenv('AZURE_SQL_PASSWORD')};"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;"
)

# Retry with backoff in case the serverless database is waking up from auto-pause
for attempt in range(1, 4):
    try:
        with pyodbc.connect(conn_str) as conn:
            row = conn.execute("SELECT SUSER_SNAME(), DB_NAME(), SYSDATETIME()").fetchone()
            print("Connected:", row)
        break
    except pyodbc.Error as e:
        print(f"Attempt {attempt} failed: {e}")
        time.sleep(10 * attempt)