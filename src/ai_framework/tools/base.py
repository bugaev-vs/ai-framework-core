from abc import ABC, abstractmethod
from typing import Any, Dict
import asyncio


class Tool(ABC):
    """Abstract base class for all tools"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def _run(self, input_text: str) -> str:
        """Main tool execution method"""
        pass

    async def run(self, input_text: str) -> str:
        """Public method with error handling"""
        try:
            result = await self._run(input_text)
            return result
        except Exception as e:
            return f"Error executing tool {self.name}: {str(e)}"

    def __call__(self, input_text: str) -> str:
        """Sync call interface"""
        return asyncio.run(self.run(input_text))