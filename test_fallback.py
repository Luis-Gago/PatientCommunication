"""
Test fallback behavior when provider fails
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add paco-api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'paco-api'))

# Set environment variables
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', '')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

from app.services.llm_service import MultiLLMService
from app.services.providers.base_provider import RateLimitError


class FakeGeminiProvider:
    """Fake provider that always fails with rate limit"""
    
    async def complete(self, messages, max_tokens, temperature=0.7):
        print("[FAKE] GeminiProvider simulating rate limit...")
        raise RateLimitError("Simulated rate limit - quota exceeded")


async def test_fallback():
    """Test that service falls back to OpenAI when Gemini fails"""
    print("=== Testing Fallback Behavior ===\n")
    
    # Create service
    service = MultiLLMService()
    
    # Replace first provider (Gemini) with fake that always fails
    print("Replacing GeminiProvider with fake that always rate limits...\n")
    service.providers[0] = FakeGeminiProvider()
    
    # Test messages
    messages = [
        {
            "role": "user",
            "content": "Say 'Fallback to OpenAI worked!' and nothing else."
        }
    ]
    
    try:
        print("Making request (should fail on Gemini, succeed on OpenAI)...\n")
        response = await service.get_chat_completion(
            messages=messages,
            max_tokens=100
        )
        
        print(f"\n✅ Fallback SUCCESS!")
        print(f"Response: {response}")
        print("\nThe system correctly switched from Gemini to OpenAI!")
        
    except Exception as e:
        print(f"\n❌ Fallback FAILED: {e}")


if __name__ == "__main__":
    asyncio.run(test_fallback())