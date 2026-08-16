import boto3
import json
import csv
from datetime import datetime, timezone, timedelta

BUCKET_NAME = "fintrust-transactions-prod"
INPUT_FILE = "high_risk_customers.csv"

s3 = boto3.client("s3")

seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

report = []

with open(INPUT_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        customer_id = row["customer_id"]
        risk_score = float(row["risk_score"])
        spike_flag = int(row["spike_flag"])

        prefix = f"customers/{customer_id}/"

        active = False

        try:
            response = s3.list_objects_v2(
                Bucket=BUCKET_NAME,
                Prefix=prefix
            )

            for obj in response.get("Contents", []):
                if obj["LastModified"] >= seven_days_ago:
                    active = True
                    break

        except Exception as e:
            print(f"Error checking {customer_id}: {e}")

        report.append({
            "customer_id": customer_id,
            "risk_score": round(risk_score, 4),
            "spike_flag": spike_flag,
            "s3_activity_7d": active,
            "account_status": "active" if active else "inactive"
        })

report_json = json.dumps(report, indent=4)

report_key = (
    f"reports/high_risk_customers_"
    f"{datetime.now().strftime('%Y%m%d')}.json"
)

s3.put_object(
    Bucket=BUCKET_NAME,
    Key=report_key,
    Body=report_json,
    ContentType="application/json"
)

print(f"Report uploaded to s3://{BUCKET_NAME}/{report_key}")