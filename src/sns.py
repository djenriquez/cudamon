import boto3
import os

def publish(message):
    client = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    response = client.publish(
        TopicArn=os.getenv('SNS_TOPIC_ARN', ''),
        Message=message,
        Subject='Miner Alert',
        MessageStructure='raw'
    )