"""
Test OpenAIProvider standalone
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add paco-api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'paco-api'))

from app.services.providers.openai_provider import OpenAIProvider

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY environment variable not set!")
    exit(1)


async def test_openai_provider():
    """Test OpenAIProvider"""
    print("Testing OpenAIProvider...\n")
    
    # Initialize provider
    provider = OpenAIProvider(api_key=OPENAI_API_KEY)
    
    # Test messages (OpenAI format)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful medical assistant."
        },
        {
            "role": "user",
            "content": "Say 'OpenAIProvider is working!' and nothing else."
        }
    ]
    
    try:
        # Call provider
        response = await provider.complete(
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"Success!")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_openai_provider())