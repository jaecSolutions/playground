import logging
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.tracing import Tracer

logger = Logger(service="my-service")
tracer = Tracer()

class CustomLogger:
    def __init__(self, log_group_name, log_stream_name):
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name

    def log_message(self, message):
        logger.info(message)

@lambda_handler_decorator
@tracer.capture_lambda_handler
@inject_lambda_context
def lambda_handler(event, context):
    custom_logger = CustomLogger(log_group_name='your-log-group', log_stream_name='your-stream-name')

    # Log custom messages using your custom logger
    custom_logger.log_message("Lambda execution started")

    # Your Lambda function logic here
    print("Executing Lambda function")

    # Log custom messages using your custom logger
    custom_logger.log_message("Lambda execution completed successfully")

    return {'statusCode': 200, 'body': 'Lambda executed successfully'}

def inject_lambda_context(func):
    def wrapper(event, context):
        # Log Lambda context information
        logger.info(f"Invoking Lambda function: {context.function_name}")
        logger.info(f"AWS Request ID: {context.aws_request_id}")
        logger.info(f"Remaining time (ms): {context.get_remaining_time_in_millis()}")

        return func(event, context)

    return wrapper
