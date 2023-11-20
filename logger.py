import logging
from aws_lambda_powertools.logging import Logger
import time
import boto3

class CustomLogger:
    def __init__(self, log_group_name, log_stream_name):
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name

        self.logger = Logger(service="my-service")
        self.setup_logging()

    def setup_logging(self):
        # Configure the logging module
        logging.basicConfig(level=logging.INFO)
        # Create a CloudWatch Logs handler and set the log group and stream
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def log_message(self, message):
        # Log the message to CloudWatch Logs
        client = boto3.client('logs')
        response = client.describe_log_streams(
            logGroupName=self.log_group_name,
            logStreamNamePrefix=self.log_stream_name
        )
        log_stream = response['logStreams'][0]['logStreamName']
        client.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=log_stream,
            logEvents=[
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': message
                },
            ]
        )

if __name__ == "__main__":
    # Example usage of the custom logger
    custom_logger = CustomLogger(log_group_name='your-log-group', log_stream_name='your-stream-name')
    custom_logger.log_message("This is a custom log message.")
