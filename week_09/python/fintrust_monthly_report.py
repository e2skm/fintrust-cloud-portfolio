"""
FinTrust Monthly Cost Report
Exercise A04 - Automating Cost Reporting with Python

Source:
CDSAP1_ Automating Cost Reporting with Python — Cost Explorer and Budgets API _ Praesignis LMS.pdf
"""

import boto3
from datetime import date

ce = boto3.client("ce", region_name="us-east-1")
s3 = boto3.client("s3")


def get_monthly_spend_by_service(year, month):
    """
    Returns a dictionary:
    {
        service_name: cost_usd
    }
    """

    start = f"{year}-{month:02d}-01"

    if month == 12:
        end = f"{year + 1}-01-01"
    else:
        end = f"{year}-{month + 1:02d}-01"

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    results = {}

    for group in response["ResultsByTime"][0]["Groups"]:
        service = group["Keys"][0]
        cost = float(
            group["Metrics"]["UnblendedCost"]["Amount"]
        )

        if cost > 0.01:
            results[service] = round(cost, 2)

    return results


class FinTrustMonthlyReport:

    BUCKET_NAME = "fintrust-cost-reports"

    def get_last_three_months(self):
        today = date.today()

        months = []

        for offset in (2, 1, 0):
            month = today.month - offset
            year = today.year

            while month <= 0:
                month += 12
                year -= 1

            months.append((year, month))

        return months

    def collect_spend_data(self):
        months = self.get_last_three_months()

        spend_data = []

        for year, month in months:
            spend_data.append(
                get_monthly_spend_by_service(year, month)
            )

        return months, spend_data

    def get_top_5_services(self, spend_data):
        averages = {}

        all_services = set()

        for month_data in spend_data:
            all_services.update(month_data.keys())

        for service in all_services:
            values = [
                month_data.get(service, 0.0)
                for month_data in spend_data
            ]

            averages[service] = sum(values) / 3

        top5 = sorted(
            averages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return [service for service, _ in top5]

    def build_report(self):
        months, spend_data = self.collect_spend_data()

        top5_services = self.get_top_5_services(spend_data)

        lines = []
        lines.append("FINTRUST MONTHLY COST REPORT")
        lines.append("=" * 95)
        lines.append(
            f"{'Service':40}"
            f"{'Month1':>12}"
            f"{'Month2':>12}"
            f"{'Month3':>12}"
            f"{'MoM %':>12}"
        )
        lines.append("-" * 95)

        for service in top5_services:

            month1 = spend_data[0].get(service, 0.0)
            month2 = spend_data[1].get(service, 0.0)
            month3 = spend_data[2].get(service, 0.0)

            if month2 > 0:
                mom_change = ((month3 - month2) / month2) * 100
            else:
                mom_change = 0.0

            sign = "+" if mom_change >= 0 else ""

            lines.append(
                f"{service[:40]:40}"
                f"{month1:>12.2f}"
                f"{month2:>12.2f}"
                f"{month3:>12.2f}"
                f"{sign}{mom_change:>11.2f}%"
            )

        return "\n".join(lines)

    def upload_report_to_s3(self, report_text):

        today = date.today()

        key = (
            f"{today.year}{today.month:02d}/"
            f"monthly_summary.txt"
        )

        s3.put_object(
            Bucket=self.BUCKET_NAME,
            Key=key,
            Body=report_text.encode("utf-8")
        )

        return f"s3://{self.BUCKET_NAME}/{key}"

    def run(self):
        report = self.build_report()

        print(report)

        location = self.upload_report_to_s3(report)

        print("\nReport uploaded to:")
        print(location)

        return location


if __name__ == "__main__":
    FinTrustMonthlyReport().run()
