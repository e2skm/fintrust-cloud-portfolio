# data_engineering_pandas_parquet_s3.py

import os
from io import StringIO
import pathlib

import pandas as pd
import pyarrow
import boto3


def load_and_transform_data():
    csv_data = """transaction_id,account_id,amount,currency,timestamp,status
txn-001,ACC-0001,1500.00,ZAR,2024-06-01 09:15:33,COMPLETED
txn-002,ACC-0002,87000.00,ZAR,2024-06-01 09:22:11,COMPLETED
txn-003,ACC-0001,250.00,ZAR,2024-06-02 14:05:02,COMPLETED
txn-004,ACC-0003,12500.00,USD,2024-06-02 16:44:55,PENDING
"""

    df = pd.read_csv(StringIO(csv_data))

    # Transformations
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["year"] = df["timestamp"].dt.year.astype(str)
    df["month"] = df["timestamp"].dt.month.astype(str).str.zfill(2)
    df["is_high_value"] = df["amount"] > 50000

    print("\nData Types:")
    print(df.dtypes)

    print("\nPreview:")
    print(df.head())

    return df


def write_partitioned_parquet(df):
    for (year, month), group in df.groupby(["year", "month"]):
        path = (
            f"fintrust_processed/year={year}/month={month}/"
            f"transactions.parquet"
        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        group.drop(columns=["year", "month"]).to_parquet(
            path,
            engine="pyarrow",
            index=False
        )

        print(f"Written: {path} ({len(group)} rows)")


def inspect_parquet():
    parquet_file = (
        "fintrust_processed/year=2024/month=06/"
        "transactions.parquet"
    )

    df_check = pd.read_parquet(
        parquet_file,
        engine="pyarrow"
    )

    print("\nParquet Data Types:")
    print(df_check.dtypes)

    print("\nParquet Data:")
    print(df_check)

    return df_check


def upload_partitions_to_s3(bucket_name, region="af-south-1"):
    s3 = boto3.client("s3", region_name=region)

    for file_path in pathlib.Path(".").glob(
        "fintrust_processed/**/*.parquet"
    ):
        s3_key = (
            "transactions/"
            + str(file_path)
            .replace("fintrust_processed/", "")
            .replace("\\", "/")
        )

        s3.upload_file(
            str(file_path),
            bucket_name,
            s3_key
        )

        print(f"Uploaded s3://{bucket_name}/{s3_key}")


def list_s3_objects(bucket_name, region="af-south-1"):
    s3 = boto3.client("s3", region_name=region)

    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(
        Bucket=bucket_name,
        Prefix="transactions/"
    ):
        for obj in page.get("Contents", []):
            size_kb = obj["Size"] // 1024
            print(f"{obj['Key']} ({size_kb} KB)")


def pandas_queries(df):
    print("\nHigh-Value Transactions")
    high_value = df[df["is_high_value"]]

    print(
        high_value[
            ["account_id", "amount", "currency"]
        ]
    )

    print(
        f"\nHigh-value transaction count: "
        f"{len(high_value)}"
    )

    print("\nTotal Amount by Currency")
    by_currency = (
        df.groupby("currency")["amount"]
        .sum()
        .reset_index()
    )

    by_currency.columns = [
        "currency",
        "total_amount"
    ]

    print(by_currency)


def main():
    df = load_and_transform_data()

    write_partitioned_parquet(df)

    parquet_df = inspect_parquet()

    pandas_queries(parquet_df)

    # Uncomment and configure if S3 access is available:
    # bucket_name = "fintrust-processed"
    # upload_partitions_to_s3(bucket_name)
    # list_s3_objects(bucket_name)


if __name__ == "__main__":
    main()
``