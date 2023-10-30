import boto3
import re
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


def content_management(event, context):
    try:
        response = s3.get_object(
            Bucket='chatgpt-test-bucket',
            Key='generated-content.txt'
        )
        content = response['Body'].read().decode()

        # Simple corporate appropriateness filter
        inappropriate_words = ["example_bad_word1", "example_bad_word2"]
        for word in inappropriate_words:
            content = re.sub(word, "[REDACTED]", content, flags=re.IGNORECASE)

        # Save filtered content back to S3
        s3.put_object(
            Bucket='chatgpt-test-bucket',
            Key='filtered-content.txt',
            Body=content
        )
    except Exception as e:
        logger.error(f"Error in content_management: {e}")
        return {
            'statusCode': 500,
            'error': str(e)
        }

    return {
        'statusCode': 200,
        'content': content
    }
