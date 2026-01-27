"""
LLM Service for chat completions
"""
from typing import List, Dict, Any, Optional
import os
from groq import AsyncGroq

from app.core.config import get_settings

settings = get_settings()


class LLMService:
    """Service for interacting with Groq LLM provider"""

    def __init__(self):
        """Initialize Groq client"""
        self.groq_client = None

        # Initialize Groq if API key is available
        if settings.GROQ_API_KEY:
            self.groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        else:
            raise ValueError("GROQ_API_KEY is required for LLM service")

    async def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Get chat completion from Groq LLM provider
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (e.g., 'llama-3.3-70b-versatile', 'mixtral-8x7b-32768')
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the LLM
            
        Returns:
            Response content as string
        """
        if not self.groq_client:
            raise ValueError("Groq API key not configured")

        # Make API call to Groq
        response = await self.groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return response.choices[0].message.content


# Global instance
llm_service = LLMService()
