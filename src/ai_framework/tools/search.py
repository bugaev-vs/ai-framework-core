from .base import Tool
import asyncio
import random


class SearchTool(Tool):
    """Mock search tool for demonstration"""
    
    def __init__(self):
        super().__init__(
            name="search",
            description="Searches for information. Use for finding facts or data."
        )
        self._mock_responses = [
            "According to recent studies, the topic you're asking about is quite complex.",
            "Research indicates that this subject has multiple perspectives.",
            "Historical data shows varying results in this area.",
            "Current trends suggest this is an evolving field.",
            "Expert opinions differ on this matter."
        ]
    
    async def _run(self, input_text: str) -> str:
        """Return mock search results"""
        await asyncio.sleep(0.1)  # Simulate API call
        response = random.choice(self._mock_responses)
        return f"Search results for '{input_text}': {response}"