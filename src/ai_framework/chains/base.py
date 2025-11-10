from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Callable
import asyncio
from ..llms.base import LLM


class Chain(ABC):
    """Abstract base class for all chains"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._callbacks: List[Callable] = []

    @abstractmethod
    async def _run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to execute the chain - must be implemented by subclasses"""
        pass

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Public method with error handling and callbacks"""
        if self.verbose:
            print(f"Running chain {self.__class__.__name__} with input: {input_data}")

        try:
            # Execute before callbacks
            for callback in self._callbacks:
                if hasattr(callback, "on_chain_start"):
                    callback.on_chain_start(input_data)

            result = await self._run(input_data)

            # Execute after callbacks
            for callback in self._callbacks:
                if hasattr(callback, "on_chain_end"):
                    callback.on_chain_end(result)

            return result

        except Exception as e:
            print(f"Error in chain execution: {e}")
            raise

    def add_callback(
        self, callback: Callable
    ) -> None:
        """Add callback for chain events"""
        self._callbacks.append(callback)

    def __call__(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sync call interface"""
        return asyncio.run(self.run(input_data))