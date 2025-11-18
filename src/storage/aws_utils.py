import boto3
import os
import requests
import logging
import json
from botocore.exceptions import ClientError
from datetime import datetime
from typing import List, Dict, Any

# Configure logging for better CloudWatch integration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- CONFIGURATION (SECURITY AND ABSTRACTION) ---
# NOTE: These variables must be set in the Docker container's environment (via docker-compose.yml)
AWS_REGION = os.environ.get("AWS_REGION", "eu-south-1")
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "cr-parser-backup")
DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE_NAME", "CR_Parsing_Results")

def get_boto3_session():
    """Returns a Boto3 Session using environment credentials (IAM Role / Env Vars)."""
    # This ensures credentials are not hardcoded.
    return boto3.Session(region_name=AWS_REGION)

def upload_file_to_s3(file_path: str, object_name: str):
    """Uploads the local PDF file to S3 for backup/audit trail."""
    session = get_boto3_session()
    s3_client = session.client('s3')
    try:
        s3_client.upload_file(file_path, S3_BUCKET, object_name)
        logger.info(f"S3 Upload Success: {object_name} backed up to {S3_BUCKET}")
    except ClientError as e:
        logger.error(f"S3 Upload Error for {object_name}: {e}")
        # We must raise here, as failure to backup the raw file is a critical failure.
        raise e

def save_result_to_dynamo(request_id: str, status: str, results: List[Dict[str, Any]] = None, error_msg: str = None):
    """Saves the processing status and results summary to DynamoDB."""
    session = get_boto3_session()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(DYNAMO_TABLE)
    
    item = {
        'PK': request_id,
        'Status': status,
        'Timestamp': datetime.now().isoformat()
    }
    
    if results:
        # Saving the count demonstrates the scale of data processed.
        item['ResultCount'] = len(results)
    if error_msg:
        item['ErrorMessage'] = error_msg
        
    try:
        table.put_item(Item=item)
        logger.info(f"DynamoDB status updated for {request_id}: {status}")
    except ClientError as e:
        logger.error(f"DynamoDB Error: {e}")
        # Failure to log status does not crash the main thread.

def send_webhook_notification(url: str, request_id: str, status: str, error: str = None):
    """Sends a completion/error notification back to the client's webhook endpoint."""
    if not url:
        return

    payload = {
        'request_id': request_id,
        'status': status
    }
    if error:
        payload['error'] = error

    try:
        requests.post(url, json=payload, timeout=5)
        logger.info(f"Webhook sent successfully for {request_id} with status {status}")
    except Exception as e:
        logger.error(f"Webhook failed for {request_id}: {e}")
