import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3

def generate_sqs_payload(bucket, key):
    # Construct the SQS payload
    payload = {
        'event': 's3:ObjectCreated:Put',
        'bucket': bucket,
        'key': key
    }

    return json.dumps(payload)

def send_sqs_message(payload, queue_url):
    # Create an SQS client
    sqs = boto3.client('sqs')

    # Send the message to the SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=payload
    )

    print(f"Message sent. MessageId: {response['MessageId']}")

class MyHandler(FileSystemEventHandler):
    def __init__(self, sqs_queue_url):
        super().__init__()
        self.sqs_queue_url = sqs_queue_url

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        print(f"New file detected: {file_path}")

        # Extract bucket and key information (modify as per your folder structure)
        folder_path, filename = os.path.split(file_path)
        bucket = 'your-s3-bucket'
        key = f"{folder_path}/{filename}"  # Modify this based on your S3 key structure

        # Generate the SQS payload
        payload = generate_sqs_payload(bucket, key)

        # Send the SQS message
        send_sqs_message(payload, self.sqs_queue_url)

def watch_folder(folder_path, sqs_queue_url):
    event_handler = MyHandler(sqs_queue_url)
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    # Replace these with your actual values
    folder_to_watch = "/path/to/your/folder"
    sqs_queue_url = 'your-sqs-queue-url'

    # Start watching the folder and sending S3 notifications to SQS
    watch_folder(folder_to_watch, sqs_queue_url)
