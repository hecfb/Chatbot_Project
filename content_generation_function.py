import boto3
import openai
import logging
import json
from botocore.exceptions import BotoCoreError, ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize clients
s3 = boto3.client('s3')
openai.api_key = "API KEY"


def generate_content(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        raise


def save_to_s3(content, bucket, key):
    try:
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=content
        )
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 error: {e}")
        raise


def lambda_handler(event, context):
    user_input = event.get("input", "Default prompt if none provided")
    try:
        generated_content = generate_content(user_input)
        save_to_s3(generated_content, "chatgpt-test-bucket",
                   "generated-content.txt")
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    return {
        "statusCode": 200,
        "content": generated_content
    }
