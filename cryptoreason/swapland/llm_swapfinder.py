import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("ASI1_API_KEY")

# ASI1-Mini LLM API endpoint
url = "https://api.asi1.ai/v1/chat/completions"

# Define headers for API requests, including authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def query_llm(query):
    """
    Queries the ASI1-Mini LLM with a given prompt and returns the model's response.

    Parameters:
        query (str): The input question or statement for the language model.

    Returns:
        str: The response from the LLM.
    
    If an error occurs during the request, the function returns the exception object.
    """
    data = {
        "messages": [{"role": "user", "content": query}],  # User input for the chat model
        "conversationId": None,  # No conversation history tracking
        "model": "asi1-mini"  # Specifies the model version to use
    }

    try:
        # Send a POST request to the LLM API with the input query
        with requests.post(url, headers=headers, json=data) as response:
            output = response.json()  # Parse the JSON response

            # Extract and return the generated message content
            return output["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        # Handle and return any request-related exceptions (e.g., network errors)
        return str(e)
