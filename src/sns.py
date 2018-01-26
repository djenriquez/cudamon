import boto3
import os
import logging
from datetime import datetime, timedelta

class SNS:
    def __init__(self):
        self.timeout = timedelta(minutes=int(os.getenv('TIMEOUT_MINS', 10)))
        self._nextAlert = datetime.utcnow()
        self._alerted = False
    
    def publish(self, message):
        if self._can_publish():
            logging.debug('Publishing SNS message: {}'.format(message))
            client = boto3.client('sns', region_name=os.getenv('AWS_REGION', 'us-east-1'))
            response = client.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN', ''),
                Message=message,
                Subject='Miner Alert',
                MessageStructure='raw'
            )
        else:
            logging.debug('Cannot publish: alerted={}, nextAlert={}'.format(self._alerted, self._nextAlert) )

    def _can_publish(self):
        if self._alerted and datetime.utcnow() < self._nextAlert:
            return False
        else:
            return True
    
    def alert(self):
        if not self._alerted:
            logging.debug('Setting alert status')
            self._alerted = True
            self._nextAlert = datetime.utcnow() + self.timeout

    def reset_alert(self):
        if self._alerted:
            logging.debug('Resetting alert status')
            self._alerted = False
