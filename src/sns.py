import boto3
import os

class SNS:
    def __init__(self):
        timeout = int(os.getenv('TIMEOUT', 10))
        alerted = False
    
    def publish(self, message):
        if self._can_publish():
            client = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'us-east-1'))
            response = client.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN', ''),
                Message=message,
                Subject='Miner Alert',
                MessageStructure='raw'
            )
            self.alerted = True

    def _can_publish(self):
        if self.alerted and self.timeout > 0:
            self.timeout -= 1
            return False
        else:
            self.reset_timeout()
            return True

    def reset_timeout(self):
        self.timeout = int(os.getenv('TIMEOUT', 10))