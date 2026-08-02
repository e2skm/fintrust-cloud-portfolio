from pathlib import Path
import sqlite3


def generate_report(conn: sqlite3.Connection, report_file: Path):
    """Generate a simple transaction summary report from the database."""

    total_transactions = conn.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    total_volume = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions"
    ).fetchone()[0]

    by_status = conn.execute(
        """
        SELECT status, COUNT(*) AS count, SUM(amount) AS volume
        FROM transactions
        GROUP BY status
        ORDER BY status
        """
    ).fetchall()

    by_type = conn.execute(
        """
        SELECT type, COUNT(*) AS count, SUM(amount) AS volume
        FROM transactions
        GROUP BY type
        ORDER BY volume DESC
        """
    ).fetchall()

    lines = [
        'FINTRUST DAILY REPORT',
        '=' * 40,
        f'Total transactions: {total_transactions}',
        f'Total volume: {total_volume:,.2f}',
        '',
        'Transactions by Status',
        '-' * 40,
    ]

    for row in by_status:
        lines.append(
            f"{row['status']}: {row['count']} transactions | Volume {row['volume']:,.2f}"
        )

    lines.extend(['', 'Transactions by Type', '-' * 40])

    for row in by_type:
        lines.append(
            f"{row['type']}: {row['count']} transactions | Volume {row['volume']:,.2f}"
        )

    report_file = Path(report_file)
    report_file.write_text(''.join(lines), encoding='utf-8')

    print(f'Report written to {report_file}')
