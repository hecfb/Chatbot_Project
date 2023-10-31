import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS S3 client
s3 = boto3.client("s3")


def publish_content(source_key, destination_key, bucket):
    try:
        s3.copy_object(
            Bucket=bucket,
            CopySource=f"{bucket}/{source_key}",
            Key=destination_key
        )
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 error: {e}")
        raise


def lambda_handler(event, context):
    try:
        publish_content("filtered-content.txt",
                        "published/filtered-content.txt", "chatgpt-test-bucket")
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    return {
        "statusCode": 200,
        "message": "Content published successfully"
    }
