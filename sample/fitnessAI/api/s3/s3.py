import boto3
from botocore.exceptions import ClientError
# from config import get_settings
# from sample.fitnessAI.api.config import get_settings
from api.config import get_settings
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

def fetch_presigned_url(file_name, fields=None, conditions=None, mp4:bool=False):
    now_time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    if mp4:
        name = f'{file_name}/{now_time}.mp4'
    else:
        name = f'{file_name}/{now_time}'

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

def create_presigned_url(key, expiration=1800):
    """Generate a presigned URL to retrieve an S3 object"""
    # Create a S3 client
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_BUCKET,
                                                            'Key': key},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print('Error generating presigned URL: ', e)
        return None
    return response