
import boto3

def get_client(service_name, **kwargs):
    return boto3.client(service_name, **kwargs)
