import os
import boto3
from dotenv import load_dotenv

BUCKET_NAME = "nutrition-raw-uploads-ab"

def load_env_variables():
    load_dotenv()
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_region": os.getenv("AWS_REGION", "us-east-2"),
    }

def get_s3_client():
    # EC2 IAM Role auto-detects credentials
    return boto3.client("s3", region_name="us-east-2")


def upload_to_s3(s3_client, uploaded_file, user_id, file_id):
    if not user_id or not file_id:
        print("Error: user_id or file_id is None")
        return False

    key = f"uploads/{user_id}/{file_id}.csv"

    try:
        s3_client.upload_fileobj(uploaded_file, BUCKET_NAME, key)
        print(f"Uploaded {file_id}.csv to S3 at {key}")
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return False
