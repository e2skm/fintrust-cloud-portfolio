from datetime import date
from pathlib import Path

import boto3

from cost_reporting import (
    get_monthly_spend_by_service,
    write_csv_report,
    write_html_report,
)


def main():
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    data = get_monthly_spend_by_service()

    csv_path = write_csv_report(
        data,
        reports_dir / "cost_report.csv",
    )

    html_path = write_html_report(
        data,
        reports_dir / "cost_report.html",
    )

    print(f"CSV report created: {csv_path}")
    print(f"HTML report created: {html_path}")

    # Upload CSV to S3
    bucket_name = "YOUR-AUDIT-BUCKET"

    today = date.today()

    key = (
        f"costreports/"
        f"{today.year}/"
        f"{today.month:02d}/"
        f"cost_report.csv"
    )

    try:
        s3 = boto3.client("s3")
        s3.upload_file(
            str(csv_path),
            bucket_name,
            key,
        )

        print(
            f"Uploaded to "
            f"s3://{bucket_name}/{key}"
        )

    except Exception as exc:
        print(f"S3 upload failed: {exc}")


if __name__ == "__main__":
    main()