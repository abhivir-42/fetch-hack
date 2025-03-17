import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get the API key from the environment variables
api_key = os.getenv("ASI1_API_KEY")

# Check if the API key is set
if not api_key:
    raise ValueError("ASI1_API_KEY environment variable is not set")

# Define the URL and payload
url = "https://api.asi1.ai/v1/chat/completions"

payload = json.dumps({
  "model": "asi1-mini",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert in Web3 technologies and decentralized systems."
    },
    {
      "role": "user",
      "content": "What is a blockchain?"
    },
    {
      "role": "assistant",
      "content": "A blockchain is a distributed, immutable ledger that records transactions across many computers. It's the underlying technology behind cryptocurrencies like Bitcoin, but its applications extend far beyond digital currencies. Each 'block' contains a set of transactions, and once verified, it's linked to the previous block, forming a chain. This design makes the data extremely difficult to alter retroactively, providing security and transparency."
    },
    {
      "role": "user",
      "content": "How does this relate to Web3?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 500
})

# Prepare headers with the API key
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {api_key}'  # Use the loaded API key here
}

# Send the request
response = requests.post(url, headers=headers, data=payload)

# Print the response
print(response.text)
