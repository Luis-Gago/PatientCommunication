"""
Gemini Flash provider implementation
"""
from typing import List, Dict
from google import genai
from .base_provider import BaseProvider, RateLimitError


class GeminiProvider(BaseProvider):
    """Google Gemini 2.5 Flash provider"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key"""
        self.client = genai.Client(api_key=api_key)
        self.model = "models/gemini-2.5-flash"
    
    async def complete(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int,
        temperature: float = 0.7
    ) -> str:
        """
        Generate completion using Gemini
        
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
            # Convert OpenAI message format to Gemini prompt
            prompt = self._convert_messages_to_prompt(messages)
            
            # Generate response (Gemini SDK is synchronous)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Detect rate limit errors
            if "429" in str(e) or "quota" in error_str or "rate" in error_str:
                raise RateLimitError(f"Gemini rate limit exceeded: {e}")
            
            # Re-raise other errors
            raise Exception(f"Gemini API error: {e}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert OpenAI-style messages to Gemini prompt
        
        OpenAI format: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        Gemini format: Single string with all messages concatenated
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"Instructions: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n\n".join(prompt_parts)