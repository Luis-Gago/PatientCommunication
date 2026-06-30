"""
Test MultiLLMService with fallback
"""
import asyncio
import sys
import os

print("=== Starting test ===")

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded .env file")
except Exception as e:
    print(f"Warning: Could not load .env: {e}")

# Check API keys are set
gemini_key = os.getenv('GEMINI_API_KEY', '')
openai_key = os.getenv('OPENAI_API_KEY', '')

print(f"GEMINI_API_KEY: {'Set ✓' if gemini_key else 'NOT SET ✗'}")
print(f"OPENAI_API_KEY: {'Set ✓' if openai_key else 'NOT SET ✗'}")

# Set environment variables for the service
os.environ['GEMINI_API_KEY'] = gemini_key
os.environ['OPENAI_API_KEY'] = openai_key

# Add paco-api to path
paco_path = os.path.join(os.path.dirname(__file__), 'paco-api')
sys.path.insert(0, paco_path)
print(f"✓ Added to path: {paco_path}")

try:
    print("\nImporting llm_service...")
    from app.services.llm_service import llm_service
    print("✓ Import successful\n")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)


async def test_multi_llm_service():
    """Test MultiLLMService"""
    print("Testing MultiLLMService...\n")
    
    # Test messages
    messages = [
        {
            "role": "system",
            "content": "You are a helpful medical assistant."
        },
        {
            "role": "user",
            "content": "Say 'MultiLLMService is working!' and nothing else."
        }
    ]
    
    try:
        # Call service (should use Gemini first)
        print("=== Test 1: Normal call ===")
        response = await llm_service.get_chat_completion(
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"\n✅ Response: {response}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Running async test...\n")
    try:
        asyncio.run(test_multi_llm_service())
        print("\n=== Test complete ===")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()