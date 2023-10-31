import boto3
import logging
import re
from botocore.exceptions import BotoCoreError, ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS S3 client
s3 = boto3.client("s3")


def fetch_content_from_s3(bucket, key):
    try:
        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )
        return response["Body"].read().decode()
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 error: {e}")
        raise


def manage_content(content):
    inappropriate_words = ["example_bad_word1", "example_bad_word2"]
    for word in inappropriate_words:
        content = re.sub(word, "[REDACTED]", content, flags=re.IGNORECASE)
    return content


def lambda_handler(event, context):
    try:
        raw_content = fetch_content_from_s3(
            "your-bucket-name", "generated-content.txt")
        managed_content = manage_content(raw_content)
        save_to_s3(managed_content, "your-bucket-name", "filtered-content.txt")
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    return {
        "statusCode": 200,
        "content": managed_content
    }
