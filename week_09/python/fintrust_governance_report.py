"""
FinTrust Governance Report
Exercise A04 - Cost Governance Automation
Source: CDSAP1_ Cost Governance Automation — Service Catalog and Tag Compliance in Python
"""

import boto3
import json
from collections import defaultdict
from datetime import date

REGION = 'af-south-1'
REQUIRED_TAGS = ['CostCentre', 'Team', 'Environment']


tagging = boto3.client('resourcegroupstaggingapi', region_name=REGION)
s3 = boto3.client('s3')


def audit_tag_compliance():
    non_compliant = {}
    total_scanned = 0

    paginator = tagging.get_paginator('get_resources')

    for page in paginator.paginate():
        for resource in page['ResourceTagMappingList']:
            total_scanned += 1
            arn = resource['ResourceARN']
            existing = {t['Key'] for t in resource.get('Tags', [])}
            missing = [t for t in REQUIRED_TAGS if t not in existing]

            if missing:
                non_compliant[arn] = missing

    return total_scanned, non_compliant


def build_governance_report():
    total_scanned, violations = audit_tag_compliance()
    initial_violations = len(violations)

    violations_by_service = defaultdict(int)
    auto_remediated = 0
    remediation_failed = 0

    for arn in violations:
        service = arn.split(':')[2] if len(arn.split(':')) > 2 else 'unknown'
        violations_by_service[service] += 1

        try:
            tagging.tag_resources(
                ResourceARNList=[arn],
                Tags={'Environment': 'Production'}
            )
            auto_remediated += 1
        except Exception:
            remediation_failed += 1

    _, remaining = audit_tag_compliance()

    report = {
        'total_scanned': total_scanned,
        'initial_violations': initial_violations,
        'auto_remediated': auto_remediated,
        'remediation_failed': remediation_failed,
        'remaining_violations': len(remaining),
        'violations_by_service': dict(violations_by_service)
    }

    report_json = json.dumps(report, indent=4)

    key = f"tag-audit/{date.today().isoformat()}.json"

    s3.put_object(
        Bucket='fintrust-governance',
        Key=key,
        Body=report_json.encode('utf-8'),
        ContentType='application/json'
    )

    print(report_json)
    print(f'Uploaded to s3://fintrust-governance/{key}')

    return report


if __name__ == '__main__':
    build_governance_report()
