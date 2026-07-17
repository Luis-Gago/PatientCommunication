"""
Groq Llama provider implementation
"""
from typing import List, Dict
from groq import AsyncGroq
from .base_provider import BaseProvider, RateLimitError


class GroqProvider(BaseProvider):
    """Groq Llama 3.3 70B provider"""
    
    def __init__(self, api_key: str):
        """Initialize Groq client with API key"""
        self.client = AsyncGroq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    async def complete(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int,
        temperature: float = 0.7
    ) -> str:
        """
        Generate completion using Groq
        
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
            # Groq uses same message format as OpenAI
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
                raise RateLimitError(f"Groq rate limit exceeded: {e}")
            
            # Re-raise other errors
            raise Exception(f"Groq API error: {e}")