import boto3
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS S3 client
s3 = boto3.client('s3')


def content_publishing(event, context):
    try:
        # Copy filtered content to the 'published' directory
        s3.copy_object(
            Bucket='chatgpt-test-bucket',
            CopySource='filtered-content.txt',
            Key='published/filtered-content.txt'
        )
    except Exception as e:
        logger.error(f"Error in content_publishing: {e}")
        return {
            'statusCode': 500,
            'error': str(e)
        }

    return {
        'statusCode': 200,
        'message': 'Content published successfully'
    }
