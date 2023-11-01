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
openai.api_key = 'api key'


def fetch_content_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode()
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 error: {e}")
        raise


def save_to_s3(content, bucket, key):
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=content)
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 error: {e}")
        raise


def manage_content(content):
    inappropriate_words = ["example_bad_word1", "example_bad_word2"]
    for word in inappropriate_words:
        content = content.replace(word, "[REDACTED]")
    return content


def publish_content(source_key, destination_key, bucket):
    try:
        s3.copy_object(
            Bucket=bucket, CopySource=f"{bucket}/{source_key}", Key=destination_key)
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 error: {e}")
        raise


def lambda_handler(event, context):
    messages = event.get('messages', [])
    role = messages[-1]['role'] if messages else None
    content = messages[-1]['content'] if messages else None

    if role == "user" and content:
        # Generate Content
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        generated_content = response['choices'][0]['message']['content']
        save_to_s3(generated_content, 'chatgpt-test-bucket',
                   'generated-content.txt')

        # Manage Content
        managed_content = manage_content(generated_content)
        save_to_s3(managed_content, 'chatgpt-test-bucket',
                   'filtered-content.txt')

        # Publish Content
        publish_content('filtered-content.txt',
                        'published/filtered-content.txt', 'chatgpt-test-bucket')

        messages.append({"role": "assistant", "content": managed_content})
    else:
        messages.append(
            {"role": "assistant", "content": "I couldn't process your request. Please try again."})

    return {
        'statusCode': 200,
        'messages': messages
    }
