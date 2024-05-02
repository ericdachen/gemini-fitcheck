import boto3
from botocore.exceptions import ClientError
from config import get_settings
from datetime import datetime


S3_REGION = 'us-east-2'
UPLOAD_EXPIRY = 1800
# S3_BUCKET = 'gemini-fit-checks'
S3_BUCKET = 'adamfitcheck'

settings = get_settings()

s3_client = boto3.client(
    "s3",
    region_name = S3_REGION,
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_key
)

def fetch_presigned_url(file_name, fields=None, conditions=None):
    now_time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    try:
        presigned_url = s3_client.generate_presigned_post(
            S3_BUCKET,
            f'{file_name}/{now_time}',
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=UPLOAD_EXPIRY,
        )
    except ClientError as error:
        print(error)
        return None
    
    return presigned_url