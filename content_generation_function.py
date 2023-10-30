import boto3
import openai
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Initialize OpenAI client
openai.api_key = 'api key'


def content_generation(event, context):
    try:
        user_input = event['input']

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )
        content = response['choices'][0]['text'].strip()

        s3.put_object(
            Bucket='chatgpt-test-bucket',
            Key='generated-content.txt',
            Body=content
        )
    except Exception as e:
        logger.error(f"Error in content_generation: {e}")
        return {
            'statusCode': 500,
            'error': str(e)
        }

    return {
        'statusCode': 200,
        'content': content
    }
