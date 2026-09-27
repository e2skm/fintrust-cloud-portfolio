import csv
from datetime import date, timedelta
from pathlib import Path

import boto3


def get_monthly_spend_by_service(months_back=1):
    """
    Return a list of dictionaries containing:
    period, service, cost_usd
    """
    ce = boto3.client("ce", region_name="us-east-1")

    today = date.today()
    start = (
        today.replace(day=1) - timedelta(days=months_back * 31)
    ).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    results = []

    for period in resp["ResultsByTime"]:
        period_start = period["TimePeriod"]["Start"]

        for group in period["Groups"]:
            service = group["Keys"][0]
            cost = float(
                group["Metrics"]["UnblendedCost"]["Amount"]
            )

            results.append(
                {
                    "period": period_start,
                    "service": service,
                    "cost_usd": cost,
                }
            )

    return results


def write_csv_report(data, output_path="cost_report.csv"):
    """
    Write cost data to CSV.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["period", "service", "cost_usd"],
        )
        writer.writeheader()
        writer.writerows(data)

    return path


def write_html_report(data, output_path="cost_report.html"):
    """
    Write a simple HTML report.
    """
    rows = "".join(
        f"<tr><td>{r['period']}</td>"
        f"<td>{r['service']}</td>"
        f"<td>${r['cost_usd']:.2f}</td></tr>"
        for r in sorted(
            data,
            key=lambda x: x["cost_usd"],
            reverse=True,
        )
        if r["cost_usd"] > 0
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>FinTrust Cost Report</title>
</head>
<body>
    <h1>Monthly Cost Report</h1>

    <table border="1">
        <tr>
            <th>Period</th>
            <th>Service</th>
            <th>Cost (USD)</th>
        </tr>

        {rows}
    </table>
</body>
</html>
"""

    path = Path(output_path)
    path.write_text(html, encoding="utf-8")

    return path


def get_per_account_spend(months_back=1):
    """
    Self-directed task from the PDF:
    Return per-account cost data joined with
    AWS Organizations account names.
    """
    ce = boto3.client("ce", region_name="us-east-1")
    org = boto3.client("organizations")

    accounts = org.list_accounts()["Accounts"]

    account_map = {
        account["Id"]: account["Name"]
        for account in accounts
    }

    today = date.today()
    start = (
        today.replace(day=1) - timedelta(days=months_back * 31)
    ).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "LINKED_ACCOUNT",
            },
            {
                "Type": "DIMENSION",
                "Key": "SERVICE",
            },
        ],
    )

    results = []

    for period in response["ResultsByTime"]:
        for group in period["Groups"]:
            account_id, service = group["Keys"]

            results.append(
                {
                    "account_id": account_id,
                    "account_name": account_map.get(
                        account_id,
                        "Unknown",
                    ),
                    "service": service,
                    "cost_usd": float(
                        group["Metrics"]["UnblendedCost"][
                            "Amount"
                        ]
                    ),
                }
            )

    return results