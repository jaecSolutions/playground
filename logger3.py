from aws_logging.logger import Logger

class CustomLogger(Logger):
    def __init__(self, *args, **kwargs):
        # You can add your custom initialization logic here
        super().__init__(*args, **kwargs)

    def custom_method(self, message):
        # Add your custom logging method here
        self.info(f"Custom Log: {message}")

# Example usage:
if __name__ == "__main__":
    # Initialize your custom logger
    custom_logger = CustomLogger(log_level="INFO", log_group="your-log-group", stream_name="your-stream-name")

    # Use the custom logger
    custom_logger.info("This is a custom log message.")
    custom_logger.custom_method("This is a custom method log message.")
