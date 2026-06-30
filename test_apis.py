"""
test script to verify API keys work
Run: python test_apis.py
"""

import httpx
import asyncio
import json
from google import genai
import os

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def test_gemini():
    print("\n=== Testing Gemini API ===")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        resp = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents="Say 'Gemini API is working!' and nothing else."
        )

        print(f"Gemini Response: {resp.text}")
        return True

    except Exception as e:
        print(f"Gemini Exception: {e}")
        return False


async def test_openai():
    """Test OpenAI API"""
    print("\n=== Testing OpenAI API ===")
    
    url = "https://api.openai.com/v1/chat/completions"
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": "Say 'OpenAI API is working!' and nothing else."
        }],
        "max_tokens": 20
    }
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result['choices'][0]['message']['content']
                print(f"OpenAI Response: {text}")
                return True
            else:
                print(f"OpenAI Error {response.status_code}: {response.text}")
                return False
                
    except Exception as e:
        print(f"OpenAI Exception: {e}")
        return False


async def main():
    print("Testing API Keys...\n")
    
    gemini_works = test_gemini()
    openai_works = await test_openai()
    
    print("\n=== Results ===")
    print(f"Gemini: {'Working' if gemini_works else 'Failed'}")
    print(f"OpenAI: {'Working' if openai_works else 'Failed'}")
    
    if gemini_works and openai_works:
        print("\n All APIs working! Ready to start implementation.")
    else:
        print("\n  Fix API keys before proceeding.")


if __name__ == "__main__":
    asyncio.run(main())