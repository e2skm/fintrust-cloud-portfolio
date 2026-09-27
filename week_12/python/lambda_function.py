import json
import tempfile
from datetime import date
from pathlib import Path

import boto3

from fintrust_migration.cost_reporting import (
    get_monthly_spend_by_service,
    write_csv_report,
    write_html_report,
)

# S3 bucket for report storage
S3_BUCKET = "fintrust-cost-reports"


def lambda_handler(event, context):
    """
    Generate monthly cost reports and upload them to S3.

    Triggered by an EventBridge schedule.
    """

    today = date.today()

    prefix = f"cost-reports/{today.year}/{today.month:02d}"

    # Get cost data
    data = get_monthly_spend_by_service(months_back=1)

    with tempfile.TemporaryDirectory() as tmpdir:

        csv_path = write_csv_report(
            data,
            f"{tmpdir}/cost_report.csv"
        )

        html_path = write_html_report(
            data,
            f"{tmpdir}/cost_report.html"
        )

        s3 = boto3.client("s3")

        uploads = [
            (csv_path, "cost_report.csv"),
            (html_path, "cost_report.html"),
        ]

        for path, key_suffix in uploads:
            s3.upload_file(
                str(path),
                S3_BUCKET,
                f"{prefix}/{key_suffix}"
            )

    return {
        "statusCode": 200,
        "body": json.dumps(
            "Reports uploaded successfully"
        ),
    }