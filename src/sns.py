import boto3
import os
from datetime import datetime, timedelta

class SNS:
    def __init__(self):
        self.timeout = timedelta(minutes=int(os.getenv('TIMEOUT_MINS', 10)))
        self.nextAlert = datetime.utcnow()
        self.alerted = False
    
    def publish(self, message):
        if self.can_publish():
            client = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'us-east-1'))
            response = client.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN', ''),
                Message=message,
                Subject='Miner Alert',
                MessageStructure='raw'
            )
            self.alerted = True
            self.nextAlert = datetime.utcnow() + self.timeout

    def can_publish(self):
        if self.alerted and datetime.utcnow() < self.nextAlert:
            return False
        else:
            return True