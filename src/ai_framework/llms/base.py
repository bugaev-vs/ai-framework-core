from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import asyncio


class LLM(ABC):
    """Abstract base class for all Language Models"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
    
    @abstractmethod
    async def _call(self, prompt: str, **kwargs) -> str:
        """Main method to call the LLM - must be implemented by subclasses"""
        pass
    
    async def call(self, prompt: str, **kwargs) -> str:
        """Public method with optional preprocessing and error handling"""
        try:
            result = await self._call(prompt, **kwargs)
            return result
        except Exception as e:
            print(f"Error calling LLM: {e}")
            raise
    
    def __call__(self, prompt: str, **kwargs) -> str:
        """Sync call interface using asyncio"""
        return asyncio.run(self.call(prompt, **kwargs))