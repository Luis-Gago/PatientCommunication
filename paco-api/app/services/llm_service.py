"""
LLM Service for chat completions
"""
from typing import List, Dict, Any, Optional
import os
from openai import AsyncOpenAI
from groq import AsyncGroq

from app.core.config import get_settings

settings = get_settings()


class LLMService:
    """Service for interacting with LLM providers (OpenAI, Groq)"""

    def __init__(self):
        """Initialize LLM clients"""
        self.openai_client = None
        self.groq_client = None

        # Initialize OpenAI if API key is available
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Initialize Groq if API key is available
        if settings.GROQ_API_KEY:
            self.groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Get chat completion from appropriate LLM provider
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (e.g., 'gpt-4o', 'llama-3.3-70b-versatile')
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the LLM
            
        Returns:
            Response content as string
        """
        # Determine which client to use based on model name
        if model.startswith(("gpt", "o1")):
            if not self.openai_client:
                raise ValueError("OpenAI API key not configured")
            client = self.openai_client
        elif model.startswith(("llama", "mixtral", "gemma")):
            if not self.groq_client:
                raise ValueError("Groq API key not configured")
            client = self.groq_client
        else:
            # Default to OpenAI
            if not self.openai_client:
                raise ValueError(f"No LLM client available for model: {model}")
            client = self.openai_client

        # Make API call
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return response.choices[0].message.content


# Global instance
llm_service = LLMService()
