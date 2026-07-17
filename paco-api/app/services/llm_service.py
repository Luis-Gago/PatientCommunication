"""
LLM Service with multiple providers and automatic fallback
"""
from typing import List, Dict, Any, Optional
import os
from app.core.config import get_settings
from .providers.base_provider import BaseProvider, RateLimitError
from .providers.gemini_provider import GeminiProvider
from .providers.openai_provider import OpenAIProvider
from .providers.groq_provider import GroqProvider

settings = get_settings()


class MultiLLMService:
    """Service with multiple LLM providers and automatic fallback"""
    
    def __init__(self):
        """Initialize all available providers in priority order"""
        self.providers: List[BaseProvider] = []
        self.current_index = 0
        
        # Add providers in priority order (Gemini first for free tier)
        if settings.GEMINI_API_KEY:
            self.providers.append(GeminiProvider(api_key=settings.GEMINI_API_KEY))
            print("[LLM] Initialized GeminiProvider")
        
        if settings.OPENAI_API_KEY:
            self.providers.append(OpenAIProvider(api_key=settings.OPENAI_API_KEY))
            print("[LLM] Initialized OpenAIProvider")
        
        # Keep Groq as fallback if available
        if settings.GROQ_API_KEY:
            self.providers.append(GroqProvider(api_key=settings.GROQ_API_KEY))
            print("[LLM] Initialized GroqProvider")
        
        if not self.providers:
            raise ValueError("No LLM API keys configured. Set GEMINI_API_KEY or OPENAI_API_KEY")
        
        print(f"[LLM] {len(self.providers)} provider(s) available")
    
    async def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-3.3-70b-versatile",  # Ignored (for backward compatibility)
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Get chat completion with automatic provider fallback
        
        Tries providers in order until one succeeds.
        Automatically switches on rate limit errors (429).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Ignored (kept for backward compatibility)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters (ignored)
            
        Returns:
            Response content as string
        """
        last_error = None
        attempts = 0
        max_attempts = len(self.providers)
        
        # Try all providers
        while attempts < max_attempts:
            provider = self.providers[self.current_index]
            provider_name = provider.__class__.__name__
            
            try:
                print(f"[LLM] Attempt {attempts + 1}/{max_attempts}: Using {provider_name}")
                
                response = await provider.complete(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                print(f"[LLM] Success with {provider_name}")
                return response
                
            except RateLimitError as e:
                print(f"[LLM] {provider_name} rate limited, switching to next provider...")
                last_error = e
                # Switch to next provider
                self.current_index = (self.current_index + 1) % len(self.providers)
                attempts += 1
                continue
                
            except Exception as e:
                print(f"[LLM] {provider_name} error: {e}")
                last_error = e
                # Try next provider
                self.current_index = (self.current_index + 1) % len(self.providers)
                attempts += 1
                continue
        
        # All providers failed
        raise Exception(f"All {max_attempts} LLM provider(s) failed. Last error: {last_error}")


# Global instance (backward compatible with existing code)
llm_service = MultiLLMService()