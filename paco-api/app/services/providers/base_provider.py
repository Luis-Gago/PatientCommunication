"""
Base provider class for LLM providers
"""
from typing import List, Dict
from abc import ABC, abstractmethod


class RateLimitError(Exception):
    """Raised when API rate limit is hit"""
    pass


class BaseProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    @abstractmethod
    async def complete(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int,
        temperature: float = 0.7
    ) -> str:
        """
        Make API call to LLM provider
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Response text as string
            
        Raises:
            RateLimitError: When 429 error or quota exceeded
        """
        pass