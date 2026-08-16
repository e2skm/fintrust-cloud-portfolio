import json
import boto3
from datetime import datetime

iam = boto3.client('iam')
ec2 = boto3.client('ec2', region_name='af-south-1')


# -----------------------------
# IAM MFA Audit
# -----------------------------
def get_users_without_mfa():
    violations = []

    paginator = iam.get_paginator('list_users')

    for page in paginator.paginate():
        for user in page['Users']:
            username = user['UserName']

            try:
                iam.get_login_profile(UserName=username)
                has_console_access = True
            except iam.exceptions.NoSuchEntityException:
                has_console_access = False

            if not has_console_access:
                continue

            mfa_devices = iam.list_mfa_devices(
                UserName=username
            )['MFADevices']

            if len(mfa_devices) == 0:
                violations.append({
                    'username': username,
                    'created': user['CreateDate'].isoformat(),
                    'last_activity': str(
                        user.get('PasswordLastUsed', 'never')
                    )
                })

    return violations


# -----------------------------
# Security Group Audit
# -----------------------------
RESTRICTED_PORTS = {22, 3389, 5432, 3306, 1521}
OPEN_CIDR = '0.0.0.0/0'


def check_sg_exposure(sg):
    findings = []

    sg_id = sg['GroupId']
    sg_name = sg.get('GroupName', sg_id)

    for rule in sg.get('IpPermissions', []):
        from_port = rule.get('FromPort', 0)
        to_port = rule.get('ToPort', 65535)

        for ip_range in rule.get('IpRanges', []):
            if ip_range['CidrIp'] == OPEN_CIDR:

                exposed_ports = [
                    p for p in RESTRICTED_PORTS
                    if from_port <= p <= to_port
                ]

                if exposed_ports or (from_port == 0 and to_port == 65535):
                    findings.append({
                        'sg_id': sg_id,
                        'sg_name': sg_name,
                        'port_range': f"{from_port}-{to_port}",
                        'cidr': OPEN_CIDR,
                        'severity': (
                            'CRITICAL'
                            if from_port == 0
                            else 'HIGH'
                        )
                    })

    return findings


def get_open_security_groups():
    findings = []

    paginator = ec2.get_paginator(
        'describe_security_groups'
    )

    for page in paginator.paginate():
        for sg in page['SecurityGroups']:
            findings.extend(check_sg_exposure(sg))

    return findings


# -----------------------------
# CHALLENGE:
# Stale Access Key Audit
# -----------------------------
def get_stale_access_keys(max_age_days=90):
    findings = []

    paginator = iam.get_paginator('list_users')

    for page in paginator.paginate():
        for user in page['Users']:
            username = user['UserName']

            response = iam.list_access_keys(
                UserName=username
            )

            for key in response['AccessKeyMetadata']:
                age_days = (
                    datetime.utcnow()
                    - key['CreateDate'].replace(tzinfo=None)
                ).days

                if age_days > max_age_days:
                    findings.append({
                        'username': username,
                        'access_key_id': key['AccessKeyId'],
                        'status': key['Status'],
                        'created': key['CreateDate'].isoformat(),
                        'age_days': age_days
                    })

    return findings


# -----------------------------
# Save Report to S3
# -----------------------------
def save_report_to_s3(bucket, findings):
    s3 = boto3.client('s3')

    today = datetime.utcnow().strftime('%Y/%m/%d')
    key = f"security-audit/{today}/findings.json"

    report = {
        'report_date': datetime.utcnow().isoformat(),
        'account_id': boto3.client(
            'sts'
        ).get_caller_identity()['Account'],
        'findings': findings
    }

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(
            report,
            indent=2,
            default=str
        ),
        ContentType='application/json',
        ServerSideEncryption='aws:kms'
    )

    print(f"Report saved to s3://{bucket}/{key}")


# -----------------------------
# Run All Audits
# -----------------------------
findings = {
    'iam_mfa_violations': get_users_without_mfa(),
    'sg_open_port_violations': get_open_security_groups(),
    'iam_stale_access_keys': get_stale_access_keys(90)
}

save_report_to_s3(
    'fintrust-audit-reports',
    findings
)