import os
import json
import boto3
import logging

# These are set in environment variables
# In lambda, set these in the Configuration tab
QUEUE_URL = os.getenv('QUEUE_URL')
REGION_NAME = os.getenv('REGION_NAME')
VALIDATION_KEY = os.getenv('VALIDATION_KEY')
VALIDATION_VALUE = os.getenv('VALIDATION_VALUE')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs', region_name=REGION_NAME)

def lambda_handler(event, context):
    headers = event.get('headers', {})
    
    if VALIDATION_KEY not in headers or headers[VALIDATION_KEY] != VALIDATION_VALUE:
        return {
            'statusCode': 403,
            'body': f"Validation failed. Invalid validation key or value provided in headers"
        }

    body = json.loads(event.get('body', '{}'))

    message = {
        'body': body,
        'headers': headers
    }
    
    logger.info(f"Sending event: {json.dumps(message)}")

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    print(f"Message sent to SQS! MessageID is {response['MessageId']}")

    return {
        'statusCode': 200,
        'body': f"Message sent to SQS! MessageID is {response['MessageId']}"
    }
