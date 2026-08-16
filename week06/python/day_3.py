import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")


def is_public_access_blocked(s3_client, bucket_name):
    """
    Returns True only if all four Public Access Block
    settings are enabled.
    """
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        config = response["PublicAccessBlockConfiguration"]

        return all([
            config.get("BlockPublicAcls", False),
            config.get("IgnorePublicAcls", False),
            config.get("BlockPublicPolicy", False),
            config.get("RestrictPublicBuckets", False),
        ])

    except s3_client.exceptions.NoSuchPublicAccessBlockConfiguration:
        return False

    except ClientError:
        return False


def is_encrypted(s3_client, bucket_name):
    """
    Returns True if default server-side encryption
    is configured on the bucket.
    """
    try:
        s3_client.get_bucket_encryption(Bucket=bucket_name)
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code in (
            "ServerSideEncryptionConfigurationNotFoundError",
            "NoSuchBucket"
        ):
            return False

        raise


def get_bucket_region(s3_client, bucket_name):
    """
    Returns the bucket region.
    """
    response = s3_client.get_bucket_location(Bucket=bucket_name)
    return response["LocationConstraint"] or "us-east-1"


# Report Header
print(
    f"{'Bucket Name':45} "
    f"{'Created':12} "
    f"{'Region':15} "
    f"{'Public Access':15} "
    f"{'Encryption'}"
)

print("-" * 105)

# Get all buckets
response = s3.list_buckets()

for bucket in response["Buckets"]:
    name = bucket["Name"]
    created = bucket["CreationDate"].strftime("%Y-%m-%d")

    region = get_bucket_region(s3, name)

    public_status = (
        "SAFE"
        if is_public_access_blocked(s3, name)
        else "EXPOSED"
    )

    encryption_status = (
        "ENCRYPTED"
        if is_encrypted(s3, name)
        else "UNENCRYPTED"
    )

    print(
        f"{name:45} "
        f"{created:12} "
        f"{region:15} "
        f"{public_status:15} "
        f"{encryption_status}"
    )