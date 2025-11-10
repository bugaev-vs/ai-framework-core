from typing import List, Dict, Any, Optional
from ..chains.base import Chain
from ..tools.base import Tool
from ..llms.base import LLM
import asyncio


class SimpleAgent(Chain):
    """Simple agent that can use tools based on LLM decisions"""

    def __init__(self, llm: LLM, tools: List[Tool], **kwargs):
        super().__init__(**kwargs)
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}

    async def _run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic with tool usage"""
        user_input = input_data.get("input", "")

        # Simple tool selection logic
        tool_to_use = self._select_tool(user_input)

        if tool_to_use:
            tool_result = await self.tools[tool_to_use].run(user_input)

            # Create enhanced prompt with tool result
            enhanced_prompt = f"""
Original question: {user_input}
Tool result: {tool_result}

Based on the tool result, provide a comprehensive answer:
"""
            final_answer = await self.llm.call(enhanced_prompt)

            return {
                "input": user_input,
                "tool_used": tool_to_use,
                "tool_result": tool_result,
                "final_answer": final_answer,
            }
        else:
            # No tool used, just LLM response
            llm_response = await self.llm.call(user_input)
            return {
                "input": user_input,
                "tool_used": None,
                "final_answer": llm_response,
            }

    def _select_tool(self, user_input: str) -> Optional[str]:
        """Improved rule-based tool selection"""
        user_input_lower = user_input.lower()

        # Математические ключевые слова и операторы
        math_keywords = [
            "calculate",
            "compute",
            "solve",
            "math",
            "equation",
            "formula",
            "+",
            "-",
            "*",
            "/",
        ]
        has_math_keyword = any(word in user_input_lower for word in math_keywords)

        # Проверяем на наличие чисел и математических операторов
        has_numbers = any(char.isdigit() for char in user_input)
        has_operators = any(op in user_input for op in ["+", "-", "*", "/"])

        # Для калькулятора: должны быть числа И (операторы ИЛИ математические ключевые слова)
        if has_numbers and (has_operators or has_math_keyword):
            return "calculator"

        # Поисковые ключевые слова
        search_keywords = [
            "search for",
            "find information",
            "look up",
            "information about",
            "what is",
            "who is",
            "tell me about",
            "capital of",
            "history of",
        ]
        if any(word in user_input_lower for word in search_keywords):
            return "search"

        # Вопросы "what is" без математического контекста → поиск
        if user_input_lower.startswith("what is") and not has_numbers:
            return "search"

        return None