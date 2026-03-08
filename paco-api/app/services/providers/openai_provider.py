"""
OpenAI GPT-4o-mini provider implementation
"""
from typing import List, Dict
from openai import AsyncOpenAI
from .base_provider import BaseProvider, RateLimitError


class OpenAIProvider(BaseProvider):
    """OpenAI GPT-4o-mini provider"""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client with API key"""
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    async def complete(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int,
        temperature: float = 0.7
    ) -> str:
        """
        Generate completion using OpenAI
        
        Args:
            messages: OpenAI-style messages format
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
            
        Raises:
            RateLimitError: On rate limit (429)
        """
        try:
            # OpenAI uses the same message format, so no conversion needed
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Detect rate limit errors
            if "429" in str(e) or "rate_limit" in error_str or "quota" in error_str:
                raise RateLimitError(f"OpenAI rate limit exceeded: {e}")
            
            # Re-raise other errors
            raise Exception(f"OpenAI API error: {e}")