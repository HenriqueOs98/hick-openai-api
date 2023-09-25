import os
import boto3
import logging
from src.function_call import openai_function_call
from src.lambda_logger import LambdaLogger  # Import the LambdaLogger class

# Initialize the logger
logger = LambdaLogger(log_level=logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    s3_record = event['Records'][0]['s3']
    bucket_name = s3_record['bucket']['name']
    object_key = s3_record['object']['key']

    object_from_event = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    object_content = object_from_event['Body'].read().decode('utf-8')
        
    openai_function_call()
