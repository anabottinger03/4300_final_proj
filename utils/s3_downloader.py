import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client('s3')

def get_processed_data(bucket_name, key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    body = obj['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(body))
    return df

def get_latest_processed_key(bucket_name, user_id):
    prefix = f"uploads/{user_id}/"
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' not in response or len(response['Contents']) == 0:
        raise ValueError("No processed files found for this user.")

    latest_file = max(response['Contents'], key=lambda x: x['LastModified'])

    return latest_file['Key']

def get_all_processed_keys(bucket_name, user_id):
    prefix = f"uploads/{user_id}/"
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' not in response or len(response['Contents']) == 0:
        raise ValueError("No processed files found for this user.")

    keys = [obj['Key'] for obj in response['Contents']]
    return keys
