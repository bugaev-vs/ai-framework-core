from .base import LLM
import asyncio
import time


class FakeLLM(LLM):
    """Fake LLM for testing - returns predefined responses"""
    
    def __init__(self, responses: Dict[str, str] = None, delay: float = 0.1):
        super().__init__(model_name="fake")
        self.responses = responses or {}
        self.delay = delay
        self.call_count = 0
    
    async def _call(self, prompt: str, **kwargs) -> str:
        """Return predefined response or echo the prompt"""
        self.call_count += 1
        
        # Simulate processing time
        if self.delay > 0:
            await asyncio.sleep(self.delay)
        
        # Return predefined response or echo the prompt
        return self.responses.get(prompt, f"Echo: {prompt}")