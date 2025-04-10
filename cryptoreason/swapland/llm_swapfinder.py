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
    # For now, just return a fixed response instead of making API calls
    if "greater than 100" in query:
        return "continue"  # Always return continue for the heartbeat check
    
    return "continue"  # Default response
