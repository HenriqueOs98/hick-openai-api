import openai
import os
import logging

from src.lambda_logger import LambdaLogger  # Import the LambdaLogger class

# Initialize the logger
logger = LambdaLogger(log_level=logging.INFO)


def openai_function_call():
    
    article = "BRASIL ES NUMERO UNO"
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    functions = [
        {
            "name": "write_post",
            "description": "Shows the title and summary of some text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the text output."
                    },
                    "summary": {
                        "type": "string",
                        "description": "Summary of the text output."
                    }
                }
            }
        }
    ]
    
    # The request to the ChatGPT API.
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages = [
            {
                "role": "system",
                "content": "You are a useful assistant."
            },
            {
                "role": "user",
                "content": f"Here is an article: {article}. Please return a title and summary."
            }
        ],
        functions = functions,
        function_call = {
            "name": functions[0]["name"]
        }
    )
    print(response)
    logging.info(response)