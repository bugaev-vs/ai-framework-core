from typing import Any, Dict
from .base import Chain
from ..llms.base import LLM


class SimpleLLMChain(Chain):
    """Simple chain that formats prompt and calls LLM"""
    
    def __init__(self, llm: LLM, prompt_template: str, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm
        self.prompt_template = prompt_template
    
    async def _run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format prompt and call LLM"""
        # Format prompt with input data
        formatted_prompt = self.prompt_template.format(**input_data)
        
        # Call LLM
        llm_response = await self.llm.call(formatted_prompt)
        
        return {
            "input": input_data,
            "prompt": formatted_prompt,
            "output": llm_response
        }
    
    def format_prompt(self, input_data: Dict[str, Any]) -> str:
        """Format prompt without executing the chain"""
        return self.prompt_template.format(**input_data)