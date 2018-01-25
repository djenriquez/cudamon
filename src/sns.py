import boto3
import os

def publish(message):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn=os.getenv('SNS_TOPIC_ARN', ''),
        Message=message,
        Subject='Miner Alert',
        MessageStructure='raw'
    )