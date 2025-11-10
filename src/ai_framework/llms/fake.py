from .base import LLM
from typing import Dict, Any
import asyncio


class FakeLLM(LLM):
    """Fake LLM for testing that provides contextual responses"""
    
    def __init__(self, response_prefix: str = "AI: "):
        self.response_prefix = response_prefix
    
    async def call(self, prompt: str, **kwargs: Any) -> str:
        """Provide contextual responses based on prompt content"""
        
        prompt_lower = prompt.lower()
        
        # ПРОСТАЯ И НАДЕЖНАЯ ЛОГИКА
        if "calculate" in prompt_lower and "110" in prompt:
            return "The calculation shows that 25 multiplied by 4 equals 100, and adding 10 gives us 110. This is a straightforward arithmetic operation."
        
        elif "artificial intelligence" in prompt_lower:
            return "Based on the search results about artificial intelligence: AI is a revolutionary field focused on creating machines that can think, learn, and solve problems like humans."
        
        elif "capital of france" in prompt_lower:
            return "According to the search results: The capital of France is Paris, renowned for its extraordinary art, architecture, and culture."
        
        elif "joke" in prompt_lower:
            return "Why don't scientists trust atoms? Because they make up everything! 🎭"
        
        # ОТВЕТ ПО УМОЛЧАНИЮ
        return f"{self.response_prefix}I understand your request and will provide a helpful response."
    
    async def call_with_metadata(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Provide response with metadata"""
        response = await self.call(prompt, **kwargs)
        return {
            "content": response,
            "prompt": prompt,
            "model": "fake-llm",
            "usage": {
                "prompt_tokens": len(prompt),
                "completion_tokens": len(response),
                "total_tokens": len(prompt) + len(response)
            }
        }