# main.py
from pathlib import Path
from fintrust_pipeline.loader   import load_csv
from fintrust_pipeline.database import setup_database, insert_transactions
from fintrust_pipeline.reporter import generate_report  # you will create this

CSV_FILE    = Path(r"C:\Users\***********\Downloads\fintrust-cloud-portfolio\week_04\day_3\transactions.csv")
DB_FILE     = Path(r"C:\Users\***********\Downloads\fintrust-cloud-portfolio\week_04\day_3\fintrust_analytics.db")
REPORT_FILE = Path(r"C:\Users\***********\Downloads\fintrust-cloud-portfolio\week_04\day_3\daily_report.txt")

if __name__ == "__main__":
    valid_rows, invalid_rows = load_csv(CSV_FILE)
    print(f"Valid: {len(valid_rows)}  Invalid: {len(invalid_rows)}")

    conn = setup_database(DB_FILE)
    inserted, skipped = insert_transactions(conn, valid_rows)
    print(f"Inserted: {inserted}  Skipped: {skipped}")

    generate_report(conn, REPORT_FILE)
    conn.close()
