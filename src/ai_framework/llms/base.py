# src/ai_framework/llms/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict


class LLM(ABC):
    """Abstract base class for all Language Models"""
    
    @abstractmethod
    async def call(self, prompt: str, **kwargs: Any) -> str:  # ⬅️ сделать call абстрактным
        """Main method to call the LLM with a prompt"""
        pass
    
    async def call_with_metadata(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Call LLM and return response with metadata"""
        content = await self.call(prompt, **kwargs)
        return {
            "content": content,
            "model": self.__class__.__name__
        }