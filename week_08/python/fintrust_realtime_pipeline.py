#!/usr/bin/env python3
"""
FinTrust Real-time Data Pipelines with Kinesis and OpenSearch
Based on the lab activities A02, A03 and A04.
"""

import json
import uuid
import datetime
import base64

try:
    import boto3
except ImportError:
    boto3 = None

try:
    from opensearchpy import OpenSearch
except ImportError:
    OpenSearch = None

REGION = 'af-south-1'
STREAM_NAME = 'transaction-stream'

# -----------------------------
# A02 - Kinesis Producer
# -----------------------------

if boto3:
    kinesis = boto3.client('kinesis', region_name=REGION)
else:
    kinesis = None


def publish_transaction(account_id, amount, currency, tx_type):
    event = {
        'transaction_id': str(uuid.uuid4()),
        'account_id': account_id,
        'amount': amount,
        'currency': currency,
        'type': tx_type,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    response = kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(event).encode('utf-8'),
        PartitionKey=account_id
    )

    return response['SequenceNumber'], response['ShardId']


def publish_batch(transactions):
    records = [
        {
            'Data': json.dumps(txn).encode('utf-8'),
            'PartitionKey': txn['account_id']
        }
        for txn in transactions
    ]

    response = kinesis.put_records(
        StreamName=STREAM_NAME,
        Records=records
    )

    failed = response['FailedRecordCount']

    if failed > 0:
        print(f'Warning: {failed} records failed')

    return len(records) - failed


# -----------------------------
# A03 - OpenSearch Indexing
# -----------------------------


def create_opensearch_client(host, username='admin', password='CHANGE_ME'):
    if OpenSearch is None:
        raise ImportError('opensearch-py is not installed')

    return OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=(username, password),
        use_ssl=True,
        verify_certs=True
    )



def index_security_event(client):
    doc = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'event_type': 'SUSPICIOUS_LOGIN',
        'account_id': 'ACC-0001',
        'source_ip': '41.13.45.22',
        'country': 'NG',
        'risk_score': 87
    }

    index_name = f"fintrust-security-{datetime.date.today().strftime('%Y-%m')}"

    response = client.index(index=index_name, body=doc)
    print(f"Indexed document: {response['_id']}")

    query = {
        'query': {
            'range': {
                'risk_score': {
                    'gte': 80
                }
            }
        }
    }

    results = client.search(index=index_name, body=query)

    for hit in results['hits']['hits']:
        print(hit['_source'])

    return index_name



def verify_index(client, index_name):
    indices = client.indices.get('fintrust-*')

    for name in indices:
        print(f'Index: {name}')

    count = client.count(index=index_name)
    print(f"Total documents: {count['count']}")


# -----------------------------
# A04 - Lambda-style Decoder
# -----------------------------


def lambda_handler(event, context):
    for record in event['Records']:
        raw = base64.b64decode(record['kinesis']['data'])
        transaction = json.loads(raw.decode('utf-8'))

        print(
            f"Received: {transaction['transaction_id']} | "
            f"Account: {transaction['account_id']} | "
            f"Amount: {transaction['amount']} {transaction['currency']}"
        )


# -----------------------------
# Demo Execution
# -----------------------------

if __name__ == '__main__':
    simulated_event = {
        'Records': [
            {
                'kinesis': {
                    'data': base64.b64encode(
                        json.dumps(
                            {
                                'transaction_id': 'txn-test-001',
                                'account_id': 'ACC-0001',
                                'amount': 15000.00,
                                'currency': 'ZAR',
                                'type': 'PAYMENT'
                            }
                        ).encode()
                    ).decode()
                }
            }
        ]
    }

    lambda_handler(simulated_event, None)
