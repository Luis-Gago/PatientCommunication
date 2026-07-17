"""
Test GeminiProvider standalone
"""
import asyncio
import sys
import os

# Add paco-api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'paco-api'))

from app.services.providers.gemini_provider import GeminiProvider

# Get API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set!")
    print("Set it first: set GEMINI_API_KEY=your_key_here")
    exit(1)


async def test_gemini_provider():
    """Test GeminiProvider"""
    print("Testing GeminiProvider...\n")
    
    # Initialize provider
    provider = GeminiProvider(api_key=GEMINI_API_KEY)
    
    # Test messages (OpenAI format)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful medical assistant."
        },
        {
            "role": "user",
            "content": "Say 'GeminiProvider is working!' and nothing else."
        }
    ]
    
    try:
        # Call provider
        response = await provider.complete(
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"Success")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_gemini_provider())